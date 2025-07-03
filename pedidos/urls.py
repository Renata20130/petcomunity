from django.urls import path
from .views import panel_farmacia_pedidos

urlpatterns = [
    path('panel/pedidos/', panel_farmacia_pedidos, name='panel_farmacia_pedidos'),
]
