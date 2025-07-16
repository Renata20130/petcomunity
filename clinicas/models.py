from django.db import models
from accounts.models import Profile
from django.contrib.auth.models import User
from django.conf import settings

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

class Tutor(models.Model):
    nombre_tutor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    ESPECIE_CHOICES = [
        ('perro', 'Canino'),
        ('gato', 'Felino'),
        ('otro', 'Otro'),
    ]

    nombre_mascota = models.CharField(max_length=100)

    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    raza = models.CharField(max_length=100, blank=True, null=True) 
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=10, choices=[('Macho', 'Macho'), ('Hembra', 'Hembra')])
    
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
        related_name='mascotas',
        null=False,
        blank=False
    )

    
    propietario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='mascotas_usuario',
        null=True,
        blank=True
    )

    clinica = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mascotas_registradas'
    )

    def __str__(self):
        return f"{self.nombre_mascota} - Tutor: {self.tutor.nombre_tutor}"


class Vacuna(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class HistorialVacuna(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    vacuna = models.ForeignKey(Vacuna, on_delete=models.CASCADE)
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.mascota} - {self.vacuna}"

class Consulta(models.Model):
    TIPO_CONSULTA_CHOICES = [
        ('general', 'General'),
        ('urgencia', 'Urgencia'),
        ('control', 'Control'),
        ('vacunacion', 'Vacunación'),
        ('otro', 'Otro'),
    ]

    ESTADO_CONSULTA_CHOICES = [
        ('abierta', 'Abierta'),
        ('cerrada', 'Cerrada'),
        ('pendiente', 'Pendiente'),
    ]

    mascota = models.ForeignKey('clinicas.Mascota', on_delete=models.CASCADE, related_name='consultas')
    clinica = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultas')    
    veterinario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas_realizadas')
    fecha = models.DateTimeField(auto_now_add=True)

    tipo_consulta = models.CharField(max_length=20, choices=TIPO_CONSULTA_CHOICES, default='general')
    motivo = models.TextField()
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True)

    proxima_cita = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CONSULTA_CHOICES, default='abierta')

    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consulta de {self.mascota.nombre} el {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        ordering = ['-fecha']


class Servicio(models.Model):
    TIPO_CHOICES = [
        ('consulta', 'Consulta'),
        ('vacuna', 'Vacuna'),
        ('cirugia', 'Cirugía'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"