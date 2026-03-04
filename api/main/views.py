import json
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.db import transaction
from main.service import service, ApiResponse
from main import forms, models

# Create your views here.
class App(View):
    def get(self, request):
        return HttpResponse("Backend Server")

class SessionView(View):
    """
        Handle authentication process
        HEAD    path(route="auth/csrf", view=views.Auth.as_view())
        GET     path(route="auth/check", view=views.Auth.as_view())
        POST    path(route="auth/login", view=views.Auth.as_view())
        DELETE  path(route="auth/logout", view=views.Auth.as_view())
    """
    
    @method_decorator(ensure_csrf_cookie)
    def head(self, request):
        """Set csrf"""
        return ApiResponse()
        
    def get(self, request):
        """Check auth"""
        response = service.check(request)
        user = request.user
        if user.is_authenticated and user.user_store:
            store = user.user_store.store
            response.update({"store": store.serialize()})
        return ApiResponse(data=response)
    
    def post(self, request):
        """Log in"""
        response = service.login(request)
        error = response.get("error", None)
        if error is not None:
            return ApiResponse(message=error, status=401)
        return ApiResponse(data=response)
    
    def delete(self, request):
        response = service.logout(request)
        return ApiResponse(data=response)

class OrderView(View):
    """
        Handle order process
        GET     path(route="order", view=views.OrderView.as_view())
        POST    path(route="order", view=views.OrderView.as_view())
        PUT     path(route="order", view=views.OrderView.as_view())
        DELETE  path(route="order", view=views.OrderView.as_view())
    """
    
    def head(self, request):
        pass
    
    def get(self, request):
        """
        Yalnizca bir masanin acik siparisi varsa
        serialize ederek doner yoksa 404 doner
        """
        table_id = request.GET.get('tableId', None)
        
        if not table_id:
            return ApiResponse(message="Masa bilgisi bulunamadı", status=403)
        
        order_set = models.Order.objects.filter(
            table=table_id,
            is_open=True
        )
        
        if not order_set.exists():
            return ApiResponse(status=404)
        
        order = order_set.first()
        return ApiResponse(data=order.serialize())
    
    def post(self, request):
        """
        Yalnizca bir masa icin acik siparis olusturur
        """
        try:
            data = json.loads(request.body)
            table_id = data.get("table", None)
            
            if not table_id:
                return ApiResponse(message="Masa bilgisi bulunamadı", status=400)
            
            # transaction.atomic baslar
            with transaction.atomic():
                # Bir masa icin yalnizca bir tane acik siparis olur
                # Istisnai durumları engellemek ve veri butunlugu
                # saglamak icin get_or_create metodu kullanildi
                order, _ = models.Order.objects.get_or_create(table_id=table_id, is_open=True)
                return ApiResponse(data=order.serialize())
                
        except json.JSONDecodeError:
            return ApiResponse(message="Geçersiz format", status=400)
        except Exception as error:
            return ApiResponse(message=str(error), status=500)
    
    def put(self, request):
        """
        Yalnizca bir siparis istemini kaydetme islemini
        gercektlestirir
        """
        try:
            data = json.loads(request.body)

            # eger urun eklenmemisse hatali yanit doner
            items_data = data.get("items", [])
            if not items_data:
                return ApiResponse(message="Ürün eklenmemiş", status=400)
            
            # transaction.atomic baslar
            with transaction.atomic():
                ticket = models.OrderTicket.objects.create(order_id=data["order"])
                
                item_instances = []
                for item in items_data:
                    # item verilerine ticket verisi inject edilir
                    item.update({"ticket": ticket.pk})

                    form = forms.CreateOrderItemForm(data=item)
                    if form.is_valid():
                        valid_data = form.cleaned_data
                        new_item = models.OrderItem(
                            order_id=data["order"],
                            product=valid_data['product'],
                            quantity=valid_data['quantity'],
                            ticket=ticket
                        )
                        item_instances.append(new_item)
                    else:
                        error = service.get_first_error_message(form)
                        return ApiResponse(message=error, status=400)
                    
                if item_instances:
                    models.OrderItem.objects.bulk_create(item_instances)
                return ApiResponse(data=ticket.order.serialize())
            
        except json.JSONDecodeError:
            return ApiResponse(message="Geçersiz format", status=400)
        except Exception as error:
            return ApiResponse(message=str(error), status=500)
        
    def patch(self, request):
        pass
    
    def delete(self, request):
        """
        Yalnizca bir hesabi kapatma islemini
        gerceklestirir
        """
        with transaction.atomic():
            """
            Aynı anda yapilan islemler olabileceginden dolayi
            Veri butunlugu icin transaction atomik baslasin
            """
            table_id = request.GET.get('tableId', None)
        
            if not table_id:
                return ApiResponse(message="Masa bilgisi bulunamadı", status=403)
            
            # Masanin acik hesaplarini filtrele
            order_set = models.Order.objects.filter(table=table_id, is_open=True)
            
            # Bu masanin acik hesabi yoksa view sonlansin
            if not order_set.exists():
                return ApiResponse(message="Sipariş bulunamadı", status=404)            
            
            # Eger listenin en basindaki guncel olandir
            form = forms.CheckOutOrderForm(
                data={"is_open": False},
                instance=order_set.first()
            )
            
            if form.is_valid():
                """
                Form validasyonunu gectiginde siparis verilerini ve mesaji doner
                """
                form.save()
                return ApiResponse()
            
            # Validasyonu gecemezse ilk form hatasini doner
            error = service.get_first_error_message(form)
            return ApiResponse(message=error, status=400)
        
def cancel_ticket(request):
    """
    Yalnizca siparise ait bir istemin iptal islemini
    gerceklestirir
    """
    ticket_id = request.GET.get('ticketId', None)
        
    if not ticket_id:
        return ApiResponse(message="İstem bilgisi bulunamadı", status=403)
    
    with transaction.atomic():
        """
        Aynı anda yapilan islemler olabileceginden dolayi
        Veri butunlugu icin transaction atomik baslasin
        """
        # ID unique fakat hata denetimi gereklidir
        ticket = models.OrderTicket.objects.filter(id=ticket_id)
        
        # Olasi bir bulunmazlik durumunda view sonlansin
        if not ticket.exists():
            return ApiResponse(message="İstem bulunamadı", status=404)
        
        # Bir ticket bulundugunda listenin en basindaki aynı zamanda tektir
        form = forms.CancelOrderTicketForm(
            data={"is_canceled": True},
            instance=ticket.first()
        )
        
        if form.is_valid():
            """
            Form validasyonunu gectiginde siparis verilerini ve mesaji doner
            """
            ticket = form.save()
            return ApiResponse(
                data=ticket.order.serialize(),
                message="Sipariş istemi iptal edildi"
            )
        
        # Validasyonu gecemezse ilk form hatasini doner
        error = service.get_first_error_message(form)
        return ApiResponse(message=error)

def print_order(request):
    """
    Yalnizca siparisin yazdirilmasi ve yazdirma durumuyla ilgili
    islemleri yapar
    """
    table_id = request.GET.get('tableId', None)
        
    if not table_id:
        return ApiResponse(message="Masa bilgisi bulunamadı", status=403)
    
    with transaction.atomic():
        """
        Aynı anda yapilan islemler olabileceginden dolayi
        Veri butunlugu icin transaction atomik baslasin
        """
        # Masanın IDsi ve açık olma durumuyla filtrele
        # Çoklu kayıt çekme ihtimaline karşı filtreleme sorgusu
        order = models.Order.objects.filter(table_id=table_id, is_open=True)
        
        # Masaya bagli acik bir siparis bulunamazsa view sonlansın
        if not order.exists():
            return ApiResponse(message="Sipariş bulunamadı", status=404)
        
        # Masaya bagli acik bir siparis bulundugunda listenin en basindaki gunceldir
        form = forms.PrintOrderReceiptForm(
            instance=order.first(),
            data={"is_printed": True}
        )
        
        if form.is_valid():
            """
            Form validasyonunu gectiginde siparis verilerini ve mesaji doner
            """
            order = form.save()
            return ApiResponse(
                data=order.serialize(),
                message="Fiş yazdırıldı"
            )
        
        # Validasyonu gecemezse ilk form hatasini doner
        error = service.get_first_error_message(form)
        return ApiResponse(message=error, status=400)