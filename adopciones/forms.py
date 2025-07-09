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

    raza = forms.CharField( # <--- ¡CÁMBIALO A CharField!
        required=True, # Mantén esto en True si la raza debe ser obligatoria
        label='Raza',
        # Aunque sea CharField, podemos usar Select para que se renderice como dropdown
        widget=forms.Select(attrs={'id': 'razaSelect'}) 
    )

    class Meta:
        model = MascotaEnAdopcion
        fields = ['nombre', 'edad', 'unidad_edad', 'especie', 'sexo', 'descripcion', 'imagen', 'raza', 'estado'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la mascota'}),
            'edad': forms.NumberInput(attrs={'min': 0}),
            'unidad_edad': forms.Select(attrs={'class': 'form-control'}), 
            'especie': forms.Select(), # Mantén este widget tal cual
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción breve'}),
            'imagen': CustomClearableFileInput(attrs={'id': 'id_imagen'}), 
            'estado': forms.Select(attrs={'class': 'form-control'}), 
        }