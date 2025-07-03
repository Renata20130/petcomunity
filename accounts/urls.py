# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('publicar-adopcion/', views.publicar_adopcion, name='publicar_adopcion'),
    path('registro/', views.registro_cliente_view, name='registro_cliente'),
    path('registro/clinica/', views.registro_clinica_view, name='registro_clinica'),
    path('registro/farmacia/', views.registro_farmacia_view, name='registro_farmacia'),
    path('panel/clinica/', views.panel_clinica, name='panel_clinica'),
    path('panel/farmacia/', views.panel_farmacia, name='panel_farmacia'),
    path('panel/cliente/', views.panel_cliente, name='panel_cliente'),
    path('cambiar-estado/', views.cambiar_estado_mascota, name='cambiar_estado_mascota'),
    


]
