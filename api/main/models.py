from uuid import uuid4
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from main.manager import UserManager
from decimal import Decimal, ROUND_HALF_UP

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
        return self.store_categories.all()
    
    def get_tables(self):
        return self.store_tables.all()
    
    @property
    def tables(self):
        return [table.serialize() for table in self.get_tables()]
    
    @property
    def categories(self):
        return [category.serialize() for category in self.get_categories()]
    
    def serialize(self):
        return {
            "id": self.pk,
            "name": self.name,
            "tables": self.tables,
            "categories": self.categories
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
            "name": self.name,
        }

class Category(AppBaseModel):
    store = models.ForeignKey(
        to=Store,
        on_delete=models.CASCADE,
        related_name='store_categories'
    )
    
    name = models.CharField(max_length=125)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def get_products(self):
        return self.product_category.all()
    
    @property
    def products(self):
        return [product.serialize() for product in self.get_products()]

    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            "id": self.pk,
            "name": self.name,
            "products": self.products
        }

class Product(AppBaseModel):
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='product_category'
    )

    name = models.CharField(max_length=125)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    @property
    def clean_price(self):
        return self.price.quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
    
    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            "id": self.pk,
            "name": self.name,
            "price": self.price
        }

class Order(AppBaseModel):
    table = models.ForeignKey(
        to=Table,
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
        return self.order_items.all()
    
    @property
    def items(self):
        return [item.serialize() for item in self.get_items()]
    
    @property
    def amount(self):
        items = self.get_items()
        return sum([item.amount for item in items])
    
    def serialize(self):
        return {
            "id": self.pk,
            "is_open": self.is_open,
            "items": self.items,
            "amount": self.amount
        }

class OrderTicket(AppBaseModel):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_tickets',
    )

    class Meta:
        verbose_name = "Sipariş İstemi"
        verbose_name_plural = "Sipariş İstemleri"

class OrderItem(AppBaseModel):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(default=1)

    ticket = models.ForeignKey(
        to=OrderTicket,
        on_delete=models.CASCADE,
        related_name="ticket_items",
        null=True
    )

    class Meta:
        verbose_name = "Sipariş Kalemi"
        verbose_name = "Sipariş Kalemleri"

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.product.name,
            "quantity": self.quantity,
            "unit_price": self.product.price,
            "amount": self.amount
        }