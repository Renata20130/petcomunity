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

    path('pacientes/', views.listado_mascotas, name='listado_mascotas'),

    path('mascota/<int:mascota_id>/ficha/', views.ficha_clinica, name='ficha_clinica'),

    path('servicios/registrar/', views.registrar_servicio, name='registrar_servicio'),

    path('servicios/', views.listado_servicios, name='listado_servicios'),

    path('mascota/<int:mascota_id>/historial/', views.historial_medico, name='historial_medico'),

    path('consulta/<int:consulta_id>/editar/', views.editar_consulta, name='editar_consulta'),

    path('mis-mascotas/', views.mis_mascotas_cliente, name='mis_mascotas_cliente'),

    path('buscar-clinicas/', views.buscar_clinicas, name='buscar_clinicas'),



]
