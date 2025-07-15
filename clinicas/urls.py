from django.urls import path
from . import views
from reservas.views import RazaListAPIView

app_name = 'clinica'

urlpatterns = [
    path('mascota/<int:mascota_id>/ficha/', views.ficha_clinica, name='ficha_clinica'),
    path('mascota/<int:mascota_id>/vacuna/nueva/', views.agregar_vacuna, name='agregar_vacuna'),
    path('mascota/<int:mascota_id>/consulta/nueva/', views.agregar_consulta, name='agregar_consulta'),
    path('mascotas/nueva/', views.registrar_mascota, name='registrar_mascota'),

    path('api/razas/', RazaListAPIView.as_view(), name='api_razas'),

    path('consulta/nueva/', views.nueva_consulta, name='nueva_consulta'),




    
]
