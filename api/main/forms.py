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
            "ticket"
        )
    
    def save(self, commit=True):
        order = self.cleaned_data.get('order')
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')

        with transaction.atomic():
            order_item, created = models.OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                order_item.quantity += quantity
                
                if commit:
                    order_item.save()

        return order_item

class CreateOrderTicketForm(forms.ModelForm):
    class Meta:
        model = models.OrderTicket
        fields = ("order",)