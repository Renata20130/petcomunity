from django.contrib.auth.models import User
from django.db import models

from django.db import models
from django.contrib.auth.models import User

from ubicacion.models import Region, Ciudad

class Profile(models.Model):
    USER_TYPES = [
        ('cliente', 'Cliente'),
        ('clinica', 'Clínica'),
        ('farmacia', 'Farmacia'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=USER_TYPES)
    perfil_publicado = models.BooleanField(default=False)
    imagen = models.ImageField(
        upload_to='perfiles/',
        default='perfiles/default.png',
        blank=True,
        null=True
    )
    

    nombre_farmacia = models.CharField(max_length=100, null=True, blank=True)
    # Campos adicionales para clínica
    nombre_clinica = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tipo}"
