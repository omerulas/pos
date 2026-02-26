from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main import models
from main import forms

# Register your models here.
@admin.register(models.User)
class UserAdmin(UserAdmin):

    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    model = models.User
    
    list_display = ('id', 'username', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}), 
        ('Yetkiler', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)

@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(models.UserStore)
class UserStoreAdmin(admin.ModelAdmin):
    list_display = ("user", "store")

@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "name")

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "name")

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "name", "price")

@admin.register(models.Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "is_open")

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product")

@admin.register(models.OrderTicket)
class OrderTicketAdmin(admin.ModelAdmin):
    list_display = ("id",)