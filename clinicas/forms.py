from django import forms
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .models import HorarioAtencion, HistorialVacuna, Consulta
from django.forms import inlineformset_factory
from accounts.models import Profile
from .models import Mascota
from .models import Tutor
from .models import Servicio



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

class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['nombre_tutor', 'telefono', 'email', 'direccion']
        widgets = {
            # ¡ELIMINA el atributo 'name' de aquí! Django lo manejará automáticamente
            'nombre_tutor': forms.TextInput(attrs={'id': 'id_tutor_nombre'}),
            'telefono': forms.TextInput(attrs={'id': 'id_tutor_telefono'}),
            'email': forms.EmailInput(attrs={'id': 'id_tutor_email'}),
            'direccion': forms.TextInput(attrs={'id': 'id_tutor_direccion'}),
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre_mascota', 'especie', 'raza', 'edad', 'sexo', 'propietario']
        widgets = {
            # ¡ELIMINA el atributo 'name' de aquí! Django lo manejará automáticamente
            'nombre_mascota': forms.TextInput(attrs={'id': 'id_mascota_nombre'}),
            'especie': forms.Select(attrs={'id': 'id_especie'}),
            'raza': forms.Select(attrs={'id': 'id_raza', 'disabled': True}),
            'edad': forms.NumberInput(attrs={'id': 'id_edad'}),
            'sexo': forms.Select(attrs={'id': 'id_sexo'}),
            'propietario': forms.Select(attrs={'id': 'id_propietario'}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'tipo', 'descripcion', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }