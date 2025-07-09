from django.urls import path
from . import views
from .views import registrar_reserva

app_name = 'reservas'

urlpatterns = [
    path('agendar/', views.agendar_reserva, name='agendar_reserva'),
    path('registrar/', registrar_reserva, name='registrar_reserva'),
    path('cliente/pedir_hora/', views.cliente_pedir_hora, name='cliente_pedir_hora'),
    path('panel/', views.panel_reservas_clinica, name='panel_reservas_clinica'),
    path('cambiar-estado/<int:reserva_id>/<str:nuevo_estado>/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('cambiar-estado/<int:reserva_id>/<str:nuevo_estado>/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('razas_por_especie/', views.obtener_razas_por_especie, name='api_razas_por_especie'),
    


]
