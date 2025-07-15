from django.urls import path
from ubicacion.views import ciudades_por_region
from . import views
from .views import cargar_ciudades

urlpatterns = [
    path('ajax/cargar-ciudades/', cargar_ciudades, name='ajax_cargar_ciudades'),
    path('ajax/ciudades/', ciudades_por_region, name='ajax-ciudades-por-region'),
    path('api/ciudades/', views.api_ciudades, name='api_ciudades'),
    


]