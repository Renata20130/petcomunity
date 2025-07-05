from django import forms
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .models import HorarioAtencion
from django.forms import inlineformset_factory
from accounts.models import Profile

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