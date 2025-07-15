from django import forms
from .models import MascotaEnAdopcion
from django.forms.widgets import ClearableFileInput
from reservas.models import Raza
from ubicacion.models import Region, Ciudad


ESPECIE_ADOPCION_CHOICES = [
    ('', 'Selecciona una especie'), # Opción vacía por defecto
    ('perro', 'Canino'),
    ('gato', 'Felino'),
    ('otro', 'Otro'),
    # ¡Importante! Añade aquí cualquier otra especie que manejes en tu API de razas
]

def get_all_breeds_from_db():
    # Obtiene todas las razas almacenadas en tu modelo Raza
    # que presumiblemente se alimenta de tu API en la app 'reserva'.
    # Usamos .values_list('nombre', 'nombre') para obtener tuplas (valor, texto_a_mostrar)
    # que es el formato que espera ChoiceField.
    breeds = list(Raza.objects.all().values_list('nombre', 'nombre'))

    # Asegurarnos de que 'Mestizo' sea siempre una opción
    mestizo_added = False
    for value, display in breeds:
        if value.lower() == 'mestizo': # Compara de forma insensible a mayúsculas/minúsculas
            mestizo_added = True
            break
    
    if not mestizo_added:
        # Añade 'Mestizo' al principio de la lista si no existe
        # (Esto lo hará disponible en el ChoiceField para la validación).
        breeds.insert(0, ('Mestizo', 'Mestizo'))

    return breeds

class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = ''
    initial_text = ''
    input_text = 'Cambiar imagen'
    template_name = 'widgets/custom_clearable_file_input.html'

class MascotaEnAdopcionForm(forms.ModelForm):
    # Definimos especie y raza explícitamente para controlar sus widgets y choices iniciales
    especie = forms.ChoiceField(
        choices=ESPECIE_ADOPCION_CHOICES,
        label="Especie de la Mascota",
        widget=forms.Select(attrs={'id': 'id_especie', 'class': 'form-control'}) # ID y clase para CSS/JS
    )

    raza = forms.ChoiceField(
        choices=[('', 'Cargando razas...')],
        label="Raza de la Mascota",
        required=False,
        widget=forms.Select(attrs={'id': 'razaSelect', 'disabled': 'disabled', 'class': 'form-control'})
    )

    class Meta:
        model = MascotaEnAdopcion
        fields = [
            'nombre', 'edad', 'unidad_edad', 'especie', 'sexo',
            'descripcion', 'imagen', 'raza', 'estado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la mascota', 'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'unidad_edad': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción breve', 'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'id': 'id_imagen', 'class': 'form-control-file'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_possible_breeds = get_all_breeds_from_db()

        # Establece las opciones del ChoiceField para la validación
        # La primera opción será el placeholder, las demás serán las razas reales
        self.fields['raza'].choices = [('', 'Selecciona una raza')] + all_possible_breeds

        # Control del estado 'disabled' del campo raza
        if 'raza' in self.fields:
            # Si es una nueva instancia de MascotaEnAdopcion
            # Y no se ha enviado una especie (o la especie enviada no es 'perro'/'gato')
            if not self.instance.pk and (not self.data.get('especie') or self.data.get('especie') == 'otro'):
                 self.fields['raza'].widget.attrs['disabled'] = 'disabled'
            else:
                 # Quita el atributo disabled si ya hay una instancia o una especie seleccionada
                 self.fields['raza'].widget.attrs.pop('disabled', None)


    def clean(self):
        cleaned_data = super().clean()
        especie_elegida = cleaned_data.get('especie')
        
        # Si la especie es 'otro', la raza se establece a 'no_aplica'
        if especie_elegida == 'otro':
            # Asegúrate de que 'no_aplica' esté en tus opciones de raza o que tu campo
            # 'raza' en el modelo permita valores arbitrarios (lo cual hace al ser CharField).
            cleaned_data['raza'] = 'no_aplica'
        
        return cleaned_data


class FormularioAdopcion(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20, required=False)
    # Agrega aquí los campos que necesites para tu formulario

class FiltroMascotaForm(forms.Form):
    especie = forms.ChoiceField(
        choices=[('', 'Todas')] + MascotaEnAdopcion.ESPECIE_CHOICES,
        required=False
    )
    sexo = forms.ChoiceField(
        choices=[('', 'Todos')] + MascotaEnAdopcion.SEXO_CHOICES,
        required=False
    )
    edad_min = forms.IntegerField(required=False, min_value=0, label='Edad mínima')
    edad_max = forms.IntegerField(required=False, min_value=0, label='Edad máxima')
    unidad_edad = forms.ChoiceField(
        choices=[('', 'Cualquiera')] + MascotaEnAdopcion.UNIDAD_EDAD_CHOICES,
        required=False
    )
    
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        empty_label="Todas las regiones"
    )
    
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),
        required=False,
        empty_label="Todas las ciudades"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['ciudad'].queryset = Ciudad.objects.none()
        elif self.initial.get('region'):
            region = self.initial.get('region')
            self.fields['ciudad'].queryset = Ciudad.objects.filter(region=region).order_by('nombre')




