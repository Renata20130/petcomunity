from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from adopciones.models import MascotaEnAdopcion

class Raza(models.Model):
    nombre = models.CharField(max_length=100, unique=False) # El nombre de la raza (ej: Labrador)
    
    # Usamos los mismos choices que en MascotaEnAdopcion para consistencia
    # Esto asocia la raza con una especie específica (perro, gato, otro)
    especie = models.CharField(max_length=20, choices=MascotaEnAdopcion.ESPECIE_CHOICES)

    class Meta:
        # Esto asegura que no puedas tener dos veces "Labrador" para "perro"
        unique_together = ('nombre', 'especie')

    def __str__(self):
        # Muestra el nombre de la raza y el nombre legible de la especie (ej: "Labrador (Canino)")
        return f"{self.nombre} ({self.get_especie_display()})"


class Reserva(models.Model):

    ESTADOS = [
    ('pendiente', 'Pendiente'),
    ('aceptada', 'Aceptada'),
    ('rechazada', 'Rechazada'),
    ]

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
    
    creada_por_clinica = models.BooleanField(default=False)  
  
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')  # <-- este es el nuevo campo
    
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas', null=True, blank=True)


    class Meta:
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f"{self.nombre_cliente} - {self.fecha} {self.hora} ({self.nombre_mascota})"

