from django.contrib import admin
from .models import MascotaEnAdopcion
from .models import SolicitudAdopcion

@admin.register(MascotaEnAdopcion)
class MascotaEnAdopcionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'edad', 'estado', 'publicada_por', 'fecha_publicacion')
    list_filter = ('estado', 'especie')
    search_fields = ('nombre', 'descripcion')

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "email", "telefono", "fecha_envio")
    search_fields = ("nombre_completo", "email")
    list_filter = ("tipo_vivienda", "fecha_envio")