from django import forms
from .models import Reserva, User
from datetime import date
from django.contrib.auth.models import User
from accounts.models import Profile

ESPECIES_CHOICES = [
    ('', 'Selecciona una especie'),
    ('perro', 'Canino'),
    ('gato', 'Felino'),
    ('otros', 'Otros'),
]

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
    
    especie = forms.ChoiceField(
        choices=ESPECIES_CHOICES,
        label="Especie de la Mascota",
        # Puedes añadir un widget si quieres un estilo diferente para el select,
        # pero el predeterminado de Django ya funciona bien con nuestro CSS
    )

    raza = forms.ChoiceField(
        choices=[('', 'Primero selecciona una especie')], # Opciones iniciales
        label="Raza de la Mascota",
        required=False,
        widget=forms.Select(attrs={'disabled': 'disabled'}) # ¡Importante! Deshabilitado al inicio
    )

    class Meta:
        model = Reserva
        fields = ['clinica', 'nombre_cliente', 'nombre_mascota', 'especie', 'raza', 'fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        especie_elegida = cleaned_data.get('especie')
        
        # Si la especie es 'otros', forzamos la raza a 'no_aplica'
        if especie_elegida == 'otros': # Compara directamente con el valor de la opción
            cleaned_data['raza'] = 'no_aplica' 
        
        return cleaned_data