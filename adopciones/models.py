from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class MascotaEnAdopcion(models.Model):
    ESPECIE_CHOICES = [
        ('perro', 'Canino'),
        ('gato', 'Felino'),
    ]

    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
        ('desconocido', 'Desconocido'),
    ]

    UNIDAD_EDAD_CHOICES = [
        ('años', 'Años'),
        ('meses', 'Meses'),
    ]
    
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(verbose_name="Edad", help_text="Número de años o meses") 

    unidad_edad = models.CharField(
        max_length=10,
        choices=UNIDAD_EDAD_CHOICES,
        default='años', # Valor por defecto
        verbose_name="Unidad de Edad"
    )

    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mascotas/', null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    publicada_por = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('publicada', 'Publicada'), ('revisada', 'Revisada')], default='pendiente')
    raza = models.CharField(max_length=100, blank=True, null=True) # Permite que sea opcional
    
    sexo = models.CharField(
        max_length=15,
        choices=SEXO_CHOICES,
        default='desconocido',
        verbose_name="Sexo"
    )

    

    def __str__(self):
        return self.nombre
