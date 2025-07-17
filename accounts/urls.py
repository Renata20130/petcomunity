# accounts/urls.py
from django.urls import path
from . import views
from .views import panel_farmacia_pedidos
from adopciones.views import panel_solicitudes
from .views import editar_perfil_farmacia
from .views import CustomLoginView
from .views import publicar_adopcion

urlpatterns = [
    
    path('registro/', views.registro_view, name='registro'),
    path('registro/cliente/', views.registro_cliente_view, name='registro_cliente'),
    path('registro/clinica/', views.registro_clinica_view, name='registro_clinica'),
    path('registro/farmacia/', views.registro_farmacia_view, name='registro_farmacia'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('publicar-adopcion/', publicar_adopcion, name='publicar_adopcion'),
    path('cambiar-estado/', views.cambiar_estado_mascota, name='cambiar_estado_mascota'),

    path('adopciones/panel-clinica/', views.panel_clinica, name='panel_clinica'),
    path('panel/farmacia/', views.panel_farmacia, name='panel_farmacia'),
    path('panel/cliente/', views.panel_cliente, name='panel_cliente'),

    path('panel/clinica/', views.panel_clinica, name='panel_clinica'),
    path('clinica/panel/', views.panel_clinica, name='panel_clinica'),

    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('editar-perfil-cliente/', views.editar_perfil_cliente, name='editar_perfil_cliente'),
    path('clinica/editar-perfil/', views.editar_perfil_clinica, name='editar_perfil_clinica'),

    path('panel-reservas/', views.panel_reservas_clinica, name='panel_reservas_clinica'),

    path('panel-farmacia/pedidos/', panel_farmacia_pedidos, name='panel_farmacia_pedidos'),

    path('panel-solicitudes/', panel_solicitudes, name='panel_solicitudes'),

    path('farmacia/editar-perfil/', editar_perfil_farmacia, name='editar_perfil_farmacia'),

    path('login/', CustomLoginView.as_view(), name='login'),

    



]

