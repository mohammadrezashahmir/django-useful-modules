from django import forms

from user_module.models import User


class edit_user_info(forms.Form):
    user_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'متن ورودی',
        }

    ), label=' نام کاربری', error_messages={
        'required': 'این فیلد اجباری است',
    })
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'متن ورودی',
        }
    ), label='ایمیل', error_messages={
        'required': 'این فیلد اجباری است',
    })
    phone_number = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'متن ورودی',
        }
    ), label='شماره تماس', required=False)
    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'متن ورودی',
        }
    ), label='آدرس', required=False)
    image = forms.ImageField(allow_empty_file=False, widget=forms.FileInput(
        attrs={
            'class': 'w-full h-full top-0 left-0 absolute opacity-0'
        }
    ), required=False)

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super(edit_user_info, self).__init__(*args, **kwargs)

    def clean(self):
        user_name = self.cleaned_data['user_name']
        if User.objects.filter(username=user_name).exclude(id=self.user_id).exists():
            self.add_error('user_name', 'این نام کاربری از قبل ثبت شده است.')
        return self.cleaned_data
