from django import forms
from .models import MascotaEnAdopcion
from django.forms.widgets import ClearableFileInput
from .widgets import CustomClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = ''  # Oculta texto checkbox
    initial_text = ''          # Oculta texto inicial
    input_text = 'Cambiar imagen'  # Texto para el botón de subir archivo
    template_name = 'widgets/custom_clearable_file_input.html'

class MascotaEnAdopcionForm(forms.ModelForm):
    class Meta:
        model = MascotaEnAdopcion
        fields = ['nombre', 'edad', 'especie', 'descripcion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la mascota'}),
            'edad': forms.NumberInput(attrs={'min': 0}),
            'especie': forms.Select(),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción breve'}),
            'imagen': CustomClearableFileInput(),
        }