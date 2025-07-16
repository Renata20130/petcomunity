from django.contrib import admin
from .models import HorarioAtencion, Mascota, Vacuna, HistorialVacuna, Consulta
from .models import Servicio

admin.site.register(HorarioAtencion)
admin.site.register(Mascota)
admin.site.register(Vacuna)
admin.site.register(HistorialVacuna)
admin.site.register(Consulta)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio')
    list_filter = ('tipo',)
    search_fields = ('nombre',)