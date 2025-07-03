from django.urls import path
from . import views
from .views import registrar_reserva

urlpatterns = [
    path('agendar/', views.agendar_reserva, name='agendar_reserva'),
    path('registrar/', registrar_reserva, name='registrar_reserva'),
    path('registrar/', views.registrar_reserva, name='registrar_reserva'),
]
