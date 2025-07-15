from django.contrib import admin
from .models import HorarioAtencion, Mascota, Vacuna, HistorialVacuna, Consulta

admin.site.register(HorarioAtencion)
admin.site.register(Mascota)
admin.site.register(Vacuna)
admin.site.register(HistorialVacuna)
admin.site.register(Consulta)