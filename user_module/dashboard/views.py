from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from user_module.models import User
from .forms import edit_user_info


class admin_dashboard_page(View):
    def get(self, request: HttpRequest):
        current_user = request.user
        form = edit_user_info(user_id=current_user.id, initial={
            'user_name': current_user.username,
            'email': current_user.email,
            'phone_number': current_user.phone_number,
            'address': current_user.address,
            'image': current_user.image,
        })
        return render(request, 'admin/dashboard/side-menu-light-update-profile.html', context={
            'user': current_user,
            'form': form
        })

    def post(self, request):
        form = edit_user_info(request.user.id, request.POST, request.FILES)
        if form.is_valid():
            status = {
                'title': 'ویرایش اطلاعات',
                'message': 'ویرایش اطلاعات با موفقیت انجام شد',
                'icon': 'success'
            }
            email = form.cleaned_data['email']
            user_name = form.cleaned_data['user_name']
            current_user = request.user
            current_user.username = user_name
            current_user.email = email
            current_user.phone_number = form.cleaned_data['phone_number']  # assuming a profile model exists
            current_user.address = form.cleaned_data['address']  # assuming a profile model exists
            if form.cleaned_data['image']:
                current_user.image = form.cleaned_data['image']  # assuming a profile model exists
            current_user.save()
            return redirect('admin_dashboard_page')
        return render(request, 'admin/dashboard/side-menu-light-update-profile.html', context={
            'user': request.user,
            'form': form
        })
