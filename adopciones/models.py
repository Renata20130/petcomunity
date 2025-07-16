from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class MascotaEnAdopcion(models.Model):
    ESPECIE_CHOICES = [
        ('perro', 'Canino'),
        ('gato', 'Felino'),
        ('otro', 'Otro'),
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



class SolicitudAdopcion(models.Model):

    ESTADOS_SOLICITUD = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('contactado', 'Contactado'),
    ]

    mascota = models.ForeignKey(
    'MascotaEnAdopcion', 
    on_delete=models.CASCADE, 
    related_name='solicitudes',
    null=True,  # permite que sea NULL en DB
    blank=True, # permite que el formulario lo deje vacío
    )

    nombre_completo = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()

    tipo_vivienda = models.CharField(max_length=50)
    situacion_vivienda = models.CharField(max_length=20)
    permiso_arrendador = models.CharField(max_length=10, blank=True, null=True)
    num_adultos = models.IntegerField()
    num_ninos = models.IntegerField()
    edades_ninos = models.TextField(blank=True, null=True)
    otras_mascotas = models.CharField(max_length=100, blank=True, null=True)
    tiempo_solo = models.CharField(max_length=20)

    experiencia_previa = models.TextField()
    gastos_compromiso = models.CharField(max_length=30)
    esterilizacion_compromiso = models.CharField(max_length=10)
    planes_futuro = models.TextField()

    declaracion_verdadera = models.BooleanField()
    acepto_terminos = models.BooleanField()

    fecha_envio = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_SOLICITUD,
        default='pendiente'
    )

    fecha_contacto = models.DateTimeField(null=True, blank=True)
    fecha_rechazo = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Solicitud para {self.mascota.nombre} por {self.nombre_completo}"


class MascotaAbandonada(models.Model):
    ESTADO_REVISION = [
        ('pendiente', 'Pendiente de revisión'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='mascotas_abandonadas/')
    estado = models.CharField(max_length=10, choices=ESTADO_REVISION, default='pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    adoptada = models.BooleanField(default=False)

    # Usuario que reporta la mascota (cliente)
    registrada_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mascotas_reportadas')

    # Clínica que revisa y aprueba
    aprobada_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mascotas_aprobadas'
    )

    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre