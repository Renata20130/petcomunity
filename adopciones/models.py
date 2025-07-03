from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class MascotaEnAdopcion(models.Model):
    ESPECIE_CHOICES = [
        ('perro', 'Canino'),
        ('gato', 'Felino'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mascotas/', null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    publicada_por = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('publicada', 'Publicada'), ('revisada', 'Revisada')], default='pendiente')

    def __str__(self):
        return self.nombre
