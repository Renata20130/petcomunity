from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.catalogo_productos, name='catalogo_productos'),
    path('subir/', views.subir_producto, name='subir_producto'),
    path('panel/', views.panel_farmacia, name='panel_farmacia'),
    path('lista/', views.lista_productos, name='lista_productos'),
    path('panel-farmacia/', views.panel_farmacia, name='panel_farmacia'),

    path('farmacia/', views.pedidos_farmacia_view, name='pedidos_farmacia'),


    path('stock/', views.stock_productos, name='stock_productos'),

    path('farmacia/nuevo/', views.nuevo_pedido_view, name='nuevo_pedido'),

    path('mis-productos/', views.mis_productos, name='mis_productos'),
    path('editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),



]