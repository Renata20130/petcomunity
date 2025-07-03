from django.contrib import admin
from .models import MascotaEnAdopcion

@admin.register(MascotaEnAdopcion)
class MascotaEnAdopcionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'edad', 'estado', 'publicada_por', 'fecha_publicacion')
    list_filter = ('estado', 'especie')
    search_fields = ('nombre', 'descripcion')
