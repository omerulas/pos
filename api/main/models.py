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
        related_name='users',
        db_index=True
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
        related_name='store_tables',
        db_index=True
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
        related_name='store_categories',
        db_index=True
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
        related_name='product_category',
        db_index=True
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
        verbose_name='Masa',
        db_index=True
    )

    is_open = models.BooleanField(verbose_name='Açık Sipariş', default=True)

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"
        unique_together = ('table', "is_open")

    def get_tickets(self):
        """
        Siparişe ait tüm ticketları object olarak doner
        """
        return self.order_tickets.all()
    
    def get_active_tickets(self):
        """
        Siparişe ait tüm aktif ticketları object olarak doner
        """
        return self.order_tickets.filter(is_canceled=False)
    
    def get_items(self):
        """
        Siparişe ait aktif ticketların içindeki tüm kalemleri tek sorguda döner.
        """
        # Aktif ticketları alıyoruz (QuerySet olarak döner)
        active_tickets = self.get_active_tickets()
        
        # OrderItem modeline gidip, 'ticket' alanı bu aktif ticketlardan 
        # biri olanları filtreleyip getiriyoruz.
        return self.order_items.filter(ticket__in=active_tickets)
    
    @property
    def items(self):
        """
        Siparişe ait tüm aktif ticketları object olarak doner
        Bu ticketlara ait itemlar üzerinde doner
        Itemların serialize edilmiş haliyle bir liste doner
        """
        return [item.serialize() for item in self.get_items()]
    
    @property
    def tickets(self):
        """
        Siparişe ait tüm ticketları object olarak doner
        Ticketların serialize edilmiş haliyle bir liste doner
        """
        return [ticket.serialize() for ticket in self.get_tickets()]
    
    @property
    def amount(self):
        """
        Siparişe ait tüm aktif ticketları object olarak doner
        Bu ticketlara ait itemlar üzerinde doner
        Itemların tutarlarını toplayıp sayı doner
        """
        items = self.get_items()

        # Tutarları toplayıp sayı doner
        return sum([item.amount for item in items])
    
    @property
    def grouped(self):
        """
        Bir siparişe aynı üründen birden fazla kalem
        ürün girilmiş olabilir
        Siparişe ait tüm aktif ticketları object olarak doner
        Bu aynı ürün kalemlerinin miktarını derleyip
        liste şeklinde doner
        """
        # item_set List[product_id: dict] seklindedir
        item_set = {}
        
        for item in self.get_items():
            """
            Aktif ticketlar üzerinden itemlara ulaşır
            """
            product_id = item.product.id

            if product_id in item_set:
                # Eger bu urun listedeyse miktar ve tutarı guncelle
                item_set[product_id]["quantity"] += item.quantity
                item_set[product_id]["amount"] += item.amount
            else:
                # Degilse serialize edilmis halini listeye ekle
                item_data = item.serialize()
                item_set[product_id] = item_data
        
        # product_id alanını atarak sadece dict listesini doner
        return list(item_set.values())
    
    def serialize(self):
        return {
            "id": self.pk,
            "is_open": self.is_open,
            "items": self.grouped,
            "tickets": self.tickets,
            "amount": self.amount,
        }

class OrderTicket(AppBaseModel):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_tickets',
        db_index=True
    )

    is_canceled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Sipariş İstemi"
        verbose_name_plural = "Sipariş İstemleri"

    def get_items(self):
        return self.ticket_items.all()
    
    @property
    def items(self):
        return [item.serialize() for item in self.get_items()]
    
    def serialize(self):
        return {
            "id": self.pk,
            "is_canceled": self.is_canceled,
            "items": self.items
        }
    
    def cancel_ticket(self):
        self.is_canceled = True
        self.save()
        return self.order.serialize()

class OrderItem(AppBaseModel):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        db_index=True
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
        verbose_name_plural = "Sipariş Kalemleri"

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    def serialize(self):
        return {
            "name": self.product.name,
            "quantity": self.quantity,
            "unit_price": self.product.price,
            "amount": self.amount
        }