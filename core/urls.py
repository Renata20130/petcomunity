from django.urls import path
from . import views
from .views import publicar_adopcion
from accounts import views as accounts_views
from core.views import home

urlpatterns = [
    path('', views.home, name='home'),
    path('adopciones/', views.adopciones, name='adopciones'),
    path('clinicas/', views.clinicas_view, name='clinicas'),
    path('farmacias/', views.farmacias_view, name='farmacias'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('publicar-adopcion/', publicar_adopcion, name='publicar_adopcion'),
    path('login/', accounts_views.login_view, name='login'),
    path('registro/', accounts_views.registro_view, name='registro'),
    path('adopciones/', views.lista_mascotas_publicas, name='adopciones'),
    path('registro/', views.registro, name='registro'),
    path('', home, name='home')


    
]