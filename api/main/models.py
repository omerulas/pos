from uuid import uuid4
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from main.manager import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        unique=True
    )

    username = models.CharField(max_length=125, unique=True)

    email = models.EmailField(
        max_length=125,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return self.username
    
class AppBaseModel(models.Model):
    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        unique=True
    )

    class Meta:
        abstract = True

class Store(AppBaseModel):
    name = models.CharField(max_length=125)
    
    class Meta:
        verbose_name = "Mağaza"
        verbose_name_plural = "Mağazalar"

    def __str__(self):
        return self.name

    def get_categories(self):
        return self.categories.all()
    
    def get_tables(self):
        return self.store_tables.all()
    
    @property
    def tables(self):
        return [table.serialize() for table in self.get_tables()]
    
    def serialize(self):
        return {
            "id": self.pk,
            "name": self.name,
            "tables": self.tables
        }
    
class UserStore(AppBaseModel):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_store'
    )

    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name='users'
    )
    
    class Meta:
        verbose_name = "Mağaza Yetkisi"
        verbose_name_plural = "Mağaza Yetkileri"
    
    def __str__(self):
        return f"{self.user.username} {self.store.name}"

class Table(AppBaseModel):
    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name='store_tables'
    )

    name = models.CharField(max_length=125)

    class Meta:
        verbose_name = "Masa"
        verbose_name_plural = "Masalar"

    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            "id": self.pk,
            "name": self.name
        }

class Category(AppBaseModel):
    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    
    name = models.CharField(max_length=125)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def get_products(self):
        return self.products.all()

    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            "id": self.pk,
            "name": self.name
        }

class Product(AppBaseModel):
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=125)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
    
    def __str__(self):
        return self.name

class Order(AppBaseModel):
    table = models.ForeignKey(
        to=Store,
        on_delete=models.SET_NULL,
        null=True,
        related_name='table_orders',
        verbose_name='Masa'
    )

    is_open = models.BooleanField(verbose_name='Açık Sipariş', default=True)

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"
        unique_together = ('table', "is_open")

    def get_items(self):
        return self.items.all()

class OrderItem(AppBaseModel):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Sipariş Kalemi"
        verbose_name = "Sipariş Kalemleri"
