from django.urls import path
from .views import panel_farmacia_pedidos
from . import views
from .views import eliminar_del_carrito


app_name = 'pedidos'

urlpatterns = [
    path('panel/pedidos/', panel_farmacia_pedidos, name='panel_farmacia_pedidos'),
    
    path('', views.listado_productos, name='listado'),

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('pedido-confirmado/', views.pedido_confirmado, name='pedido_confirmado'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    
    path('cancelar/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido'),





]
