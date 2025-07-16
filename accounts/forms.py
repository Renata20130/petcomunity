from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from ubicacion.models import Ciudad
from ubicacion.models import Region

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa un email válido.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.profile.tipo = 'cliente'  # El registro base es siempre cliente
            user.profile.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

class RegistroClinicaForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa un email válido.")
    nombre_clinica = forms.CharField(max_length=100, required=True, label="Nombre de la Clínica")
    direccion = forms.CharField(max_length=255, required=True, label="Dirección")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono de Contacto")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nombre_clinica', 'direccion', 'telefono']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.profile.tipo = 'clinica'
            user.profile.save()
            # Si tienes un modelo Clinic asociado, podrías crear aquí la clínica:
            # Clinic.objects.create(user=user, nombre=self.cleaned_data['nombre_clinica'], ...)
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

class RegistroFarmaciaForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa un email válido.")
    nombre_farmacia = forms.CharField(max_length=100, required=True, label="Nombre de la Farmacia")
    direccion = forms.CharField(max_length=255, required=True, label="Dirección")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono de Contacto")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nombre_farmacia', 'direccion', 'telefono']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.profile.tipo = 'farmacia'
            user.profile.save()
            # Aquí podrías guardar también en un modelo Farmacia si lo tienes
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
    
class PerfilClinicaForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Correo electrónico')
    telefono = forms.CharField(max_length=20, required=True, label='Teléfono de contacto')

    class Meta:
        model = Profile
        fields = ['perfil_publicado', 'imagen', 'telefono']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['telefono'].initial = user.profile.telefono

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user
        
        print("Guardando teléfono:", self.cleaned_data.get('telefono'))  # <--- Depuración

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        profile.telefono = self.cleaned_data['telefono']

        if commit:
            user.save()
            profile.save()
            
        return profile

class EditarPerfilForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError("Este correo ya está registrado por otro usuario.")
        return email

class EditarPerfilExtendidoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['imagen', 'telefono']  

from django import forms
from accounts.models import Profile
from ubicacion.models import Region, Ciudad

class EditarPerfilFarmaciaForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Correo electrónico')

    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label='Región')
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.none(), required=False, label='Ciudad')

    class Meta:
        model = Profile
        fields = [
            'nombre_clinica', 'direccion', 'telefono', 'imagen',
            'perfil_publicado', 'region', 'ciudad'
        ]
        labels = {
            'nombre_clinica': 'Nombre de la Farmacia',
            'direccion': 'Dirección',
            'telefono': 'Teléfono de contacto',
            'imagen': 'Imagen de perfil',
            'perfil_publicado': '¿Mostrar perfil públicamente?',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.region:
            self.fields['ciudad'].queryset = Ciudad.objects.filter(region=self.instance.region).order_by('nombre')
        else:
            self.fields['ciudad'].queryset = Ciudad.objects.none()

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['nombre_clinica'].initial = user.profile.nombre_clinica
            self.fields['direccion'].initial = user.profile.direccion
            self.fields['telefono'].initial = user.profile.telefono
            self.fields['region'].initial = user.profile.region
            self.fields['ciudad'].initial = user.profile.ciudad
            self.fields['perfil_publicado'].initial = user.profile.perfil_publicado
            self.fields['imagen'].initial = user.profile.imagen

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['ciudad'].queryset = Ciudad.objects.none()
        elif self.instance and self.instance.region:
            self.fields['ciudad'].queryset = Ciudad.objects.filter(region=self.instance.region).order_by('nombre')
            if self.instance.ciudad and self.instance.ciudad not in self.fields['ciudad'].queryset:
                self.fields['ciudad'].queryset |= Ciudad.objects.filter(id=self.instance.ciudad.id)

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile.save()
        return profile


class EditarPerfilClinicaForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Correo electrónico')

    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False)
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.none(), required=False)

    class Meta:
        model = Profile
        fields = ['nombre_clinica', 'direccion', 'telefono', 'imagen', 'perfil_publicado', 'region', 'ciudad']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.region:
            self.fields['ciudad'].queryset = Ciudad.objects.filter(region=self.instance.region).order_by('nombre')
        else:
            self.fields['ciudad'].queryset = Ciudad.objects.none()

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['nombre_clinica'].initial = user.profile.nombre_clinica
            self.fields['direccion'].initial = user.profile.direccion
            self.fields['telefono'].initial = user.profile.telefono
            self.fields['region'].initial = user.profile.region
            self.fields['ciudad'].initial = user.profile.ciudad
            self.fields['perfil_publicado'].initial = user.profile.perfil_publicado
            self.fields['imagen'].initial = user.profile.imagen

        # 👇 Esta es la clave para que solo muestre las ciudades según la región seleccionada
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['ciudad'].queryset = Ciudad.objects.none()
        elif self.instance and self.instance.region:
            self.fields['ciudad'].queryset = Ciudad.objects.filter(region=self.instance.region).order_by('nombre')
            # Asegura que la ciudad seleccionada esté en el queryset
            if self.instance.ciudad and self.instance.ciudad not in self.fields['ciudad'].queryset:
                self.fields['ciudad'].queryset |= Ciudad.objects.filter(id=self.instance.ciudad.id)
        else:
            self.fields['ciudad'].queryset = Ciudad.objects.none()


    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            profile.save()
        return profile