from django.db import models
from accounts.models import Profile

class HorarioAtencion(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=15, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.profile} - {self.dia}: {self.hora_inicio} a {self.hora_fin}"
