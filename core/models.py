
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mascotas/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Clinica(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    horario = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='clinicas/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    

class MascotaAdopcion(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    publicado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)  # para que lo revise la clínica

    def __str__(self):
        return self.nombre
    

