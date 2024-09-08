from django import forms
from django.core.exceptions import ValidationError


class register_form(forms.Form):
    user_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'user_name',
            'placeholder': 'نام کاربری',

        }
    ), error_messages={
        'required': 'این فیلد اجباری است'
    })
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'email',
            'placeholder': 'ایمیل',
        }
    ), label='Email', error_messages={
        'invalid': 'ایمیل نامعتبر است',
        'required': 'این فیلد اجباری است'
    })
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'password',
            'placeholder': 'کلمه عبور',
        }
    ), label='Password', error_messages={
        'required': 'این فیلد اجباری است'
    })
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'password',
            'placeholder': 'تایید کلمه عبور',

        }
    ), label='Confirm Password', error_messages={
        'required': 'این فیلد اجباری است'
    })

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تایید کلمه عبور مغابرت دارند')


class login_form(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block',
            'id': 'email',
            'placeholder': 'ایمیل',
        }
    ), label='Email', error_messages={
        'invalid': 'ایمیل نامعتبر است',
        'required': 'این فیلد اجباری است'
    })
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'password',
            'placeholder': 'کلمه عبور',
        }
    ), label='Password', error_messages={
        'required': 'این فیلد اجباری است'
    })


class forget_password_form(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block',
            'id': 'email',
            'placeholder': 'ایمیل',
        }
    ), label='Email', error_messages={
        'invalid': 'ایمیل نامعتبر است',
        'required': 'این فیلد اجباری است'
    })


class reset_password_form(forms.Form):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'password',
            'placeholder': 'کلمه عبور جدید',
        }
    ), label='Password', error_messages={
        'required': 'این فیلد اجباری است'
    })
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'password',
            'placeholder': 'تایید کلمه عبور',

        }
    ), label='Confirm Password', error_messages={
        'required': 'این فیلد اجباری است'
    })

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تایید کلمه عبور مغابرت دارند')


class change_password_form(forms.Form):
    current_password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'current_password',
            'placeholder': 'متن ورودی',
        }
    ), label='کلمه عبور فعلی', error_messages={
        'required': 'این فیلد اجباری است'
    })
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'new_password',
            'placeholder': 'متن ورودی',
        }
    ), label='کلمه عبور جدید', error_messages={
        'required': 'این فیلد اجباری است'
    })
    confirm_new_password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={
            'class': 'intro-x login__input form-control py-3 px-4 border-gray-300 block mt-4',
            'id': 'confirm_new_password',
            'placeholder': 'متن ورودی',

        }
    ), label='تایید کلمه عبور', error_messages={
        'required': 'این فیلد اجباری است'
    })

    def clean_confirm_new_password(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_new_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تایید کلمه عبور مغابرت دارند')
