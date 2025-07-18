from django.urls import path
from . import views
from .views import registrar_reserva
from .views import RazaListAPIView

app_name = 'reservas'

urlpatterns = [
    
    path('agendar/', views.agendar_reserva, name='agendar_reserva'),
    path('registrar/', registrar_reserva, name='registrar_reserva'),
    path('cliente/pedir_hora/', views.cliente_pedir_hora, name='cliente_pedir_hora'),
    path('panel/', views.panel_reservas_clinica, name='panel_reservas_clinica'),
    path('cambiar-estado/<int:reserva_id>/<str:nuevo_estado>/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('cambiar-estado/<int:reserva_id>/<str:nuevo_estado>/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('razas_por_especie/', views.obtener_razas_por_especie, name='api_razas_por_especie'),
    
    path('razas/', RazaListAPIView.as_view(), name='api_razas_list'),
    path('razas_por_especie/', views.obtener_razas_por_especie, name='api_razas_por_especie'),


    path('mis-reservas/', views.mis_reservas, name='mis_reservas_cliente'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva_cliente, name='cancelar_reserva_cliente'),




]
