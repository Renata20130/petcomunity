from django import forms
from .models import Mascota
from .models import Clinica
from .models import MascotaAdopcion

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'edad', 'descripcion', 'imagen']

class ClinicaForm(forms.ModelForm):
    class Meta:
        model = Clinica
        fields = ['nombre', 'direccion', 'telefono', 'horario', 'descripcion', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class MascotaAdopcionForm(forms.ModelForm):
    class Meta:
        model = MascotaAdopcion
        fields = ['nombre', 'edad', 'descripcion', 'imagen']