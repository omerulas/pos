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

    def get(self, request, table_id):
        try:
            table = models.Table.objects.get(id=table_id)
            order = models.Order.objects.get(table=table)
            return ApiResponse(data=order.serialize())
        except models.Order.DoesNotExist:
            return ApiResponse(status=404)

    def post(self, request):
        data = service.data(request)
        table = models.Table.objects.get(id=data["table"])
        order, _ = models.Order.objects.get_or_create(table=table)
        return ApiResponse(data=order.serialize())

    # def put(self, request):
    #     data = service.data(request=request)
    #     ticket_data = {"order": data["order"]}
    #     msg, ticket = service.save(forms.CreateOrderTicketForm, ticket_data)
    #     print(msg, ticket)
    #     for item in data["items"]:
    #         print(item)
    #         item.update({"ticket": ticket.id})
    #         print(item)
    #         result = service.save(forms.CreateOrderItemForm, item)
    #         error = result.get("error", None)
    #         if error is not None:
    #             return ApiResponse(message=error, status=400)
    #     order = models.Order.objects.get(id=data["order"])
    #     return ApiResponse(data=order.serialize())

    def put(self, request):
        try:
            data = json.loads(request.body)

            # eger urun eklenmemisse hatali yanit doner
            items_data = data.get("items", [])
            if not items_data:
                return ApiResponse(message="Ürün eklenmemiş", status=400)
            
            # transaction.atomic baslar
            with transaction.atomic():
                try:
                    # gelen veriden orderı bulur
                    order = models.Order.objects.get(id=data["order"])
                except models.Order.DoesNotExist:
                    return ApiResponse(message="Sipariş bulunamadı")
                
                ticket = models.OrderTicket.objects.create(order=order)
                
                for item in items_data:
                    form = forms.CreateOrderItemForm(data=item)
                    if form.is_valid():
                        order_item = form.save(commit=False)

                        order_item.ticket = ticket

                        order_item.save()
                    else:
                        return ApiResponse(
                            message=service.get_first_error_message(form),
                            status=400
                        )
                    
                # gelen verideki tum siparis kalemlerini olusturdugunda
                # order verilerini doner
                return ApiResponse(data=order.serialize())
        # json cozumleme hatasi alirsa
        except json.JSONDecodeError:
            return ApiResponse(message="Geçersiz format", status=400)
        # on gorulemeyen hata alirsa
        except Exception as error:
            print("Sistem hatası: ", str(error))
            return ApiResponse(message=str(error), status=500)