from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_peso_and_valor_total),
]