# ubicacion/models.py

from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='ciudades')
    nombre = models.CharField(max_length=100)

    class Meta:
        unique_together = ('region', 'nombre')

    def __str__(self):
        return f"{self.nombre} ({self.region.nombre})"
