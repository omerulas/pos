from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ('username', 'is_active')
        error_messages = {
            'username': {
                'required': "Kullanıcı için kullanıcı adı giriniz",
            }
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.User
        fields = ('username', 'is_active', 'is_staff')
        