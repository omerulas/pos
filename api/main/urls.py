from django.urls import path
from main import views

urlpatterns = [
    path(route="order", view=views.OrderView.as_view()),
    path(route="print", view=views.print_order),
    path(route="ticket", view=views.cancel_ticket),
]