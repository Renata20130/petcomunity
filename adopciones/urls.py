from django.urls import path
from . import views
from accounts.views import panel_clinica
from .views import publicar_adopcion
from .views import eliminar_adopcion
from .views import mis_postulaciones
from accounts import views as accounts_views
from .views import detalle_reporte_mascota, editar_reporte_mascota, eliminar_reporte_mascota, mis_reportes_mascota_abandonada
from adopciones.views import publicar_adopcion

app_name = 'adopciones'

urlpatterns = [
    path('panel-clinica/', accounts_views.panel_clinica, name='panel_clinica'),
    
    path('publicar/', views.publicar_adopcion, name='publicar_adopcion'),
    path('editar/<int:mascota_id>/', views.editar_adopcion, name='editar_adopcion'),
    path('eliminar/<int:pk>/', eliminar_adopcion, name='eliminar_adopcion'),
   
    path('publicas/', views.lista_mascotas_publicas, name='adopciones_publicas'),
    path('mascota/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),

    path('cambiar_estado/', views.cambiar_estado_mascota, name='cambiar_estado_mascota'),
    path('mis_publicaciones/', views.mis_publicaciones_clinica, name='mis_publicaciones_clinica'),

    path('mascotas/<int:mascota_id>/actualizar_estado/', views.actualizar_estado_mascota, name='actualizar_estado_mascota'),
    
    path('solicitar/<int:mascota_id>/', views.formulario_adopcion_view, name='formulario_adopcion_mascota'),
    path("procesar-solicitud/", views.procesar_solicitud, name="procesar_solicitud"),
    path('solicitud-exitosa/', views.solicitud_exitosa, name='solicitud_exitosa'),

    path("solicitud/<int:solicitud_id>/", views.detalle_solicitud, name="detalle_solicitud"),

    path('solicitudes/<int:solicitud_id>/actualizar-estado/', views.actualizar_estado_solicitud, name='actualizar_estado_solicitud'),

    path('mis-postulaciones/', mis_postulaciones, name='mis_postulaciones'),

    path('registrar-abandono/', views.registrar_mascota_abandonada, name='registrar_abandono'),

    path('revisar/', views.panel_revision_mascotas, name='panel_revision'),
    path('aprobar/<int:mascota_id>/', views.aprobar_mascota, name='aprobar_mascota'),
    path('rechazar/<int:mascota_id>/', views.rechazar_mascota, name='rechazar_mascota'),

    path('', views.lista_mascotas_adopcion, name='lista_adopciones'),

    path('registrar/', views.registrar_mascota_abandonada, name='registrar_mascota'),

    path('mis-reportes/', views.mis_reportes_mascota_abandonada, name='mis_reportes_mascota_abandonada'),
    path('registrar/', views.registrar_mascota_abandonada, name='registrar_mascota_abandonada'),
    path('reportes/<int:id>/', detalle_reporte_mascota, name='detalle_reporte_mascota'),
    path('reportes/<int:id>/editar/', editar_reporte_mascota, name='editar_reporte_mascota'),
    path('reportes/<int:id>/eliminar/', eliminar_reporte_mascota, name='eliminar_reporte_mascota'),


    path('reportes/pendientes/', views.lista_reportes_pendientes, name='lista_reportes_pendientes'),
    path('reportes/revisar/<int:reporte_id>/', views.revisar_reporte, name='revisar_reporte'),





]