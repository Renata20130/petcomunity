from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'farmacia', 'fecha_creacion')
    search_fields = ('nombre',)
    list_filter = ('farmacia',)

