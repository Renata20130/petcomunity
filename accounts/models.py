from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPES = [
        ('cliente', 'Cliente'),
        ('clinica', 'Clínica'),
        ('farmacia', 'Farmacia'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=USER_TYPES)
    imagen = models.ImageField(
        upload_to='perfiles/',
        default='perfiles/default.png',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.tipo}"
