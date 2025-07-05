from django.urls import path
from . import views
from accounts.views import panel_clinica
from .views import publicar_adopcion
from .views import eliminar_adopcion


urlpatterns = [
    path('panel-clinica/', views.panel_clinica, name='panel_clinica'),
    path('panel-clinica/', panel_clinica, name='panel_clinica'),
    
    path('publicar-adopcion/', views.publicar_adopcion, name='publicar_adopcion'),
    path('publicar-adopcion/', publicar_adopcion, name='publicar_adopcion'),
    path('editar/<int:mascota_id>/', views.editar_adopcion, name='editar_adopcion'),
    path('eliminar/<int:pk>/', eliminar_adopcion, name='eliminar_adopcion'),
   
    path('publicas/', views.lista_mascotas_publicas, name='adopciones_publicas'),
    path('mascota/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),

    
    
]