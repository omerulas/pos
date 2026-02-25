from django.urls import path
from main import views

urlpatterns = [
    path(route="order", view=views.OrderView.as_view()),
    path(route="order/<uuid:table_id>", view=views.OrderView.as_view())
]