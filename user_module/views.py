from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import usersSerializer,currentUserSerializer
from .forms import register_form, login_form, forget_password_form, reset_password_form, change_password_form
from .models import User
from services_module.send_email import send_email


def user_not_access():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(reverse('main_page'))
                # todo: it must be profile page when i create the profile page
            else:
                return func(request, *args, **kwargs)

        return wrapper

    return decorator


class register_page(View):
    @method_decorator(user_not_access())
    def get(self, request):
        form = register_form()
        return render(request, 'user/signUp.html',
                      {
                          'form': form
                      }, )

    def post(self, request: HttpRequest):
        form = register_form(request.POST)
        status = {
            'title': 'فعال سازی حساب شما',
            'message': 'متاسفانه در ارسال لینک فعال سازی مشکلی پیش آمد',
            'icon': 'error',

        }
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                form.add_error('email', 'این ایمیل قبلا توسط کاربر دیگری ثبت شده است')
            else:
                user_password = form.cleaned_data.get('confirm_password')
                user_name = form.cleaned_data.get('user_name')
                new_user = User(activation_code=get_random_string(72), email=user_email, is_active=False,
                                username=user_name)
                new_user.set_password(user_password)
                send_email('فعال سازی حساب کاربری', new_user.email, {'code': new_user.activation_code},
                           'activate_account.html')
                new_user.save()
                status['message'] = f' ارسال شد {new_user.email}لینکی برای فعال سازی حساب شما به ایمیل '
                status['icon'] = 'success'

        return render(request, 'user/signUp.html', {
            'form': form,
            'status': status,
        })


def activate_account(request: HttpRequest, code):
    user: User = User.objects.filter(activation_code__iexact=code).first()
    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse('main_page'))
    else:
        raise ValidationError('چنین کاربری با این کد وجود ندارد')


class login_page(View):
    @method_decorator(user_not_access())
    def get(self, request):
        form = login_form()
        return render(request, 'user/login.html',
                      {'form': form},
                      )

    def post(self, request):
        form = login_form(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_password = form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if user.is_active:
                    is_correct = user.check_password(user_password)
                    if is_correct:
                        login(request, user)
                        return redirect(reverse('main_page'))
                    else:
                        form.add_error('email', 'ایمیل یا کلمه عبور اشتباه وارد شده است')
                        return render(request, 'user/login.html', {'form': form})
                else:
                    form.add_error('email', 'این کاربر بلاک شده است')
                    return render(request, 'user/login.html', {'form': form})
            else:
                form.add_error('email', 'ایمیل یا کلمه عبور اشتباه وارد شده است')
                return render(request, 'user/login.html', {'form': form})


class forget_password(View):
    @method_decorator(user_not_access())
    def get(self, request: HttpRequest):
        form = forget_password_form()
        return render(request, 'user/forget_password.html', {'form': form})

    def post(self, request: HttpRequest):
        form = forget_password_form(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            status = {
                'title': 'بازیابی حساب شما',
                'message': f'عملیات ارسال ایمیل ناموفق بود',
                'icon': 'error'
            }
            if user is not None:
                send_email('بازیابی حساب شما در کارگ', user_email, {'code': user.activation_code},
                           'reset_password_email.html')
                status['message'] = f'لینکی برای بازیابی حساب شما به ایمیل {user_email} ارسال شد'
                status['icon'] = 'success'
                return render(request, 'user/forget_password.html', context={
                    'status': status,
                })
            else:
                form.add_error('email', ' کاربری با این ایمیل پیدا نشد')
        return render(request, 'user/forget_password.html', {'form': form})


class reset_password(View):
    @method_decorator(user_not_access())
    def get_user(self, code):
        user = User.objects.filter(activation_code__iexact=code).first()
        if self.user is None:
            raise Http404()
        return user

    def get(self, request: HttpRequest, code):
        user = self.get_user(code)
        form = reset_password_form()
        return render(request, 'user/reset_password.html', {
            'form': form,
            'code': code,
        })

    def post(self, request: HttpRequest, code):
        user = self.get_user(code)
        form = reset_password_form(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.email_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))
        return render(request, 'user/reset_password.html', context={
            'form': form,
            'code': code
        })


class change_password(View):
    def get(self, request: HttpRequest):
        form = change_password_form()
        return render(request, 'user/change-password.html', context={
            'form': form
        })

    def post(self, request: HttpRequest):
        form = change_password_form(request.POST)
        status = {}
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            is_correct: bool = request.user.check_password(current_password)
            if is_correct:
                new_password = form.cleaned_data['new_password']
                request.user.set_password(new_password)
                status = {
                    'title': 'تغییر کلمه عبور',
                    'message': 'کلمه عبور شما با موفقیت تغییر یافت',
                    'icon': 'success'
                }
            else:
                form.add_error('current_password', 'کلمه عبور فعلی اشتباه وارد شده است')
        return render(request, 'user/change-password.html', context={
            'form': form,
            'status': status
        })


def logout_user(request: HttpRequest):
    logout(request)
    return redirect(reverse('main_page'))


class getAdminUsers(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True, is_superuser=True)
    serializer_class = usersSerializer


class currentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = currentUserSerializer(user)
        return Response(serializer.data)
