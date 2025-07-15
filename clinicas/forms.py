from django import forms
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .models import HorarioAtencion, HistorialVacuna, Consulta
from django.forms import inlineformset_factory
from accounts.models import Profile
from .models import Mascota


class HorarioAtencionForm(forms.ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = ['dia', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            raise ValidationError('La hora de fin debe ser posterior a la hora de inicio.')

HorarioAtencionFormSet = inlineformset_factory(
    Profile,
    HorarioAtencion,
    form=HorarioAtencionForm,
    can_delete=True,
    extra=1
)

class HistorialVacunaForm(forms.ModelForm):
    class Meta:
        model = HistorialVacuna
        fields = ['vacuna', 'fecha_aplicacion', 'proxima_dosis', 'observaciones']
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'proxima_dosis': forms.DateInput(attrs={'type': 'date'}),
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['mascota', 'motivo', 'diagnostico', 'tratamiento', 'notas']
        widgets = {
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control'}),
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'edad', 'sexo', 'propietario']
        widgets = {
            'especie': forms.Select(attrs={'id': 'id_especie'}),
            'raza': forms.Select(attrs={'id': 'id_raza', 'disabled': True}),
            'nombre': forms.TextInput(attrs={'id': 'id_nombre'}),
            'edad': forms.NumberInput(attrs={'id': 'id_edad'}),
            'sexo': forms.Select(attrs={'id': 'id_sexo'}),
            'propietario': forms.Select(attrs={'id': 'id_propietario'}),
        }