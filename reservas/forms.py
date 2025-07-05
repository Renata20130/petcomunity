from django import forms
from .models import Reserva
from datetime import date
from django.contrib.auth.models import User
from accounts.models import Profile

class ReservaFormClinica(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre_cliente', 'nombre_mascota', 'especie', 'raza', 'fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Motivo de la reserva'}),
        }
        
class ReservaFormCliente(forms.ModelForm):
    clinica = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__tipo='clinica', profile__perfil_publicado=True),
            label="Clínica"
        )

    class Meta:
        model = Reserva
        fields = ['clinica', 'nombre_cliente', 'nombre_mascota', 'especie', 'raza', 'fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }