from django.shortcuts import render, redirect
from .forms import MascotaForm
from .models import Mascota
from .forms import ClinicaForm
from .models import Clinica
from django.contrib import messages
from .forms import MascotaAdopcionForm
from django.contrib.auth.decorators import login_required
from adopciones.models import MascotaEnAdopcion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile  


def adopciones(request):
    mascotas = MascotaEnAdopcion.objects.filter(
        publicada_por__profile__tipo='clinica',
        estado='publicada'
    ).order_by('-fecha_publicacion')
    
    return render(request, 'adopciones.html', {'mascotas': mascotas})
def clinicas_view(request):
    if request.method == 'POST':
        form = ClinicaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clínica publicada correctamente.')
            return redirect('clinicas')
    else:
        form = ClinicaForm()

    clinicas = User.objects.filter(profile__tipo='clinica')

    return render(request, 'clinicas.html', {
        'form': form,
        'clinicas': clinicas
    })

def farmacias_view(request):
    return render(request, 'farmacias.html')


def contacto_view(request):
    return render(request, 'contacto.html')

@login_required
def publicar_adopcion(request):
    if request.method == 'POST':
        form = MascotaAdopcionForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.publicado_por = request.user
            mascota.publicado = False  # para que la clínica revise antes de publicar
            mascota.save()
            return redirect('adopciones')  # o a donde quieras
    else:
        form = MascotaAdopcionForm()
    return render(request, 'adopciones/publicar_adopcion.html', {'form': form})

def lista_mascotas_publicas(request):
    mascotas = MascotaEnAdopcion.objects.filter(estado='publicada').order_by('-fecha_publicacion')
    return render(request, 'adopciones/lista_adopciones.html', {'mascotas': mascotas})


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # o a donde quieras redirigir
    else:
        form = UserCreationForm()
    return render(request, 'accounts/registro.html', {'form': form})

def home(request):
    mascotas_clinica = MascotaEnAdopcion.objects.filter(
        publicada_por__profile__tipo='clinica',
        estado='publicada'
    )
    clinicas = User.objects.filter(profile__tipo='clinica')

    return render(request, 'home.html', {
        'mascotas_clinica': mascotas_clinica,
        'clinicas': clinicas,  # <- ESTO es lo que te faltaba
    })