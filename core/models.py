
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Clinica(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    horario = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='clinicas/', blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class UserProfile(models.Model):
    # Un usuario tiene UN perfil, y un perfil pertenece a UN usuario.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    
    # Un perfil de usuario se asocia a UNA clínica.
    # Si la clínica se elimina, el campo 'clinica' en el perfil se pone a NULL.
    # null=True y blank=True permiten que un usuario pueda no tener una clínica asignada inicialmente.
    clinica = models.ForeignKey(
        Clinica,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_asociados' # Permite acceder a los usuarios desde una clínica
    )
    
    # Puedes añadir otros campos al perfil si los necesitas (ej. rol, etc.)
    # rol = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        # Muestra el nombre de usuario y, si tiene, el nombre de la clínica
        return f"Perfil de {self.user.username} ({self.clinica.nombre if self.clinica else 'Sin Clínica'})"


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)

    edad = models.IntegerField(default=0)
    UNIDAD_EDAD_CHOICES = [
        ('meses', 'Meses'),
        ('años', 'Años'),
    ]
    unidad_edad = models.CharField(
        max_length=10,
        choices=UNIDAD_EDAD_CHOICES,
        default='años',
    )

    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mascotas/', null=True, blank=True)

    clinica = models.ForeignKey(
        Clinica,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mascotas_publicadas'
    )

    ESPECIE_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('otro', 'Otro'),
    ]
    especie = models.CharField(
        max_length=20,
        choices=ESPECIE_CHOICES,
        default='perro',
    )

    RAZA_CHOICES = [
        ('labrador', 'Labrador'),
        ('pastor_aleman', 'Pastor Alemán'),
        ('mestizo', 'Mestizo'),
        # Puedes añadir más razas aquí o en un modelo separado si necesitas mucha flexibilidad
    ]
    raza = models.CharField(
        max_length=50,
        choices=RAZA_CHOICES,
        default='mestizo',
        blank=True,
        null=True,
    )

    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    sexo = models.CharField(
        max_length=10,
        choices=SEXO_CHOICES,
        default='macho',
    )

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
    

