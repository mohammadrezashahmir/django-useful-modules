from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    activation_code = models.CharField(max_length=80, verbose_name='activation code')
    image = models.ImageField(upload_to='user_images', null=True, blank='')
    address = models.TextField(null=True, blank='')
    phone_number = models.IntegerField(null=True, blank='')
