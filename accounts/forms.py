from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

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