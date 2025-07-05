from django.db import models

# Create your models here.
class Farmacia(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    # otros campos como teléfono, horario, etc.

    def __str__(self):
        return self.nombre