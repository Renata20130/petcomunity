from django.contrib import admin
from .models import Region, Ciudad

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region')
    list_filter = ('region',)