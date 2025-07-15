from django import forms
from .models import Reserva, User
from datetime import date
from django.contrib.auth.models import User
from accounts.models import Profile
from reservas.models import Raza

ESPECIES_CHOICES = [
    ('', 'Selecciona una especie'),
    ('perro', 'Canino'),
    ('gato', 'Felino'),
    ('otros', 'Otros'),
]

def get_all_breeds_from_db():
    # Obtiene todas las razas almacenadas en tu modelo Raza
    # que presumiblemente se alimenta de tu API en la app 'reserva'.
    # Usamos .values_list('nombre', 'nombre') para obtener tuplas (valor, texto_a_mostrar)
    # que es el formato que espera ChoiceField.
    breeds = list(Raza.objects.all().values_list('id', 'nombre'))

    # Verifica si ya existe "Mestizo" por nombre
    mestizo_added = any(nombre.lower() == 'mestizo' for _, nombre in breeds)

    if not mestizo_added:
        # Añade "Mestizo" con un valor especial "-1" si no está en la base de datos
        breeds.insert(0, ('-1', 'Mestizo'))
    return breeds

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
        widget=forms.Select(attrs={'id': 'id_especie', 'class': 'form-control'}) # ID y clase para CSS/JS
    )

    raza = forms.ChoiceField(
        choices=[('', 'Cargando razas...')],
        label="Raza de la Mascota",
        required=False,
        widget=forms.Select(attrs={'id': 'razaSelect', 'disabled': 'disabled', 'class': 'form-control'})
    )

    raza = forms.ChoiceField(
        choices=[('', 'Primero selecciona una especie')], # Opciones iniciales
        label="Raza de la Mascota",
        required=False,
        widget=forms.Select(attrs={'disabled': 'disabled'}) # ¡Importante! Deshabilitado al inicio
    )

    es_urgente = forms.BooleanField(
    required=False,
    label="Atención urgente",
    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Reserva
        fields = ['clinica', 'nombre_cliente', 'nombre_mascota', 'especie', 'raza', 'fecha', 'hora', 'motivo', 'es_urgente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
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
        raza_id = cleaned_data.get('raza')

        if raza_id == '-1':
            cleaned_data['raza'] = 'Mestizo'
        elif raza_id:
            try:
                raza_obj = Raza.objects.get(id=raza_id)
                cleaned_data['raza'] = raza_obj.nombre
            except Raza.DoesNotExist:
                self.add_error('raza', 'La raza seleccionada no existe.')

        return cleaned_data