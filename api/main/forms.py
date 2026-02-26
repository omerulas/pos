from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main import models
from django.db import transaction

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ('username', 'is_active')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.User
        fields = ('username', 'is_active', 'is_staff')

class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = models.Order
        fields = ("table",)

class CreateOrderItemForm(forms.ModelForm):
    class Meta:
        model = models.OrderItem
        fields = (
            "order",
            "product",
            "quantity",
        )

class CreateOrderTicketForm(forms.ModelForm):
    class Meta:
        model = models.OrderTicket
        fields = ("order",)