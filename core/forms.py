from django import forms
from .models import Mascota
from .models import Clinica
from .models import MascotaAdopcion
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, resolve_url
from django.contrib.auth import login

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


class CustomLoginView(LoginView):
    def form_valid(self, form):
        """Redirige según tipo de usuario, ignorando 'next' si no es cliente."""
        user = form.get_user()
        login(self.request, user)

        if hasattr(user, 'profile'):
            tipo = user.profile.tipo
            if tipo == 'cliente':
                # Respetar el parámetro 'next' si viene de un cliente
                return redirect(self.get_redirect_url() or resolve_url('reservas:pedir_cita'))
            else:
                # Si es clínica o farmacia, ir siempre al home
                return redirect(resolve_url('home'))
        # Si no tiene perfil (raro), redirigir al home igual
        return redirect(resolve_url('home'))

