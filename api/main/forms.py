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

class CheckInOrderForm(forms.ModelForm):
    
    class Meta:
        model = models.Order
        fields = ("table",)
        
class PrintOrderReceiptForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ("is_printed",)
    
class CheckOutOrderForm(forms.ModelForm):
    
    class Meta:
        model = models.Order
        fields = ("is_open",)
        
    def clean(self):
        cleaned_data = super().clean()
        
        if self.instance and not self.instance.is_printed:
            raise forms.ValidationError("Hesap yazdırılmamış")
        
        return cleaned_data

class CreateOrderItemForm(forms.ModelForm):
    class Meta:
        model = models.OrderItem
        fields = (
            "order",
            "product",
            "quantity",
        )
        
class CancelOrderTicketForm(forms.ModelForm):
    class Meta:
        model = models.OrderTicket
        fields = ("is_canceled",)