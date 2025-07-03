from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Reserva(models.Model):
    clinica = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas_recibidas')
    
    nombre_cliente = models.CharField(max_length=100, default='')
    telefono_cliente = models.CharField(max_length=20, default="")
    email_cliente = models.EmailField(default="sin@email.com")
    
    nombre_mascota = models.CharField(max_length=100, default='')
    especie = models.CharField(max_length=50, blank=True, null=True)
    raza = models.CharField(max_length=100, default='')
    
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(blank=True)
    creada = models.DateTimeField(auto_now_add=True)
    
    creada_por_clinica = models.BooleanField(default=False)  # <-- nuevo campo
    
    class Meta:
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f"{self.nombre_cliente} - {self.fecha} {self.hora} ({self.nombre_mascota})"

