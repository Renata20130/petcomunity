from django.urls import include, path
from . import views
from .views import publicar_adopcion

from accounts import views as accounts_views
from core.views import home

from .views import productos_publicados
from adopciones import views as adopciones_views

app_name = 'core'  

urlpatterns = [
    path('', views.home, name='home'),
    path('adopciones/', views.adopciones, name='adopciones'),
    path('clinicas/', views.clinicas_view, name='clinicas'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('publicar-adopcion/', adopciones_views.publicar_adopcion, name='publicar_adopcion'),
    path('login/', accounts_views.login_view, name='login'),
    path('registro/', accounts_views.registro_view, name='registro'),
    path('adopciones/', views.lista_mascotas_publicas, name='adopciones'),
    path('registro/', views.registro, name='registro'),
    path('', home, name='home'),
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),
    path('productos/', productos_publicados, name='productos_publicados'),
    path('productos/', include('productos.urls', namespace='productos')),
    path('productos/', include('productos.urls')),

    path('farmacias/', views.farmacias_view, name='farmacias'),

    


]