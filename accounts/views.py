from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from adopciones.models import MascotaEnAdopcion
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from accounts.decorators import tipo_requerido
from reservas.models import Reserva

from .forms import RegistroForm, RegistroClinicaForm, RegistroFarmaciaForm  # Crearemos estos formularios separados
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})

def registro_cliente_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # Asignar tipo 'cliente'
            user.profile.tipo = 'cliente'
            user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro_cliente.html', {'form': form})

def registro_clinica_view(request):
    if request.method == 'POST':
        form = RegistroClinicaForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.profile.tipo = 'clinica'
            user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroClinicaForm()
    return render(request, 'accounts/registro_clinica.html', {'form': form})

from django.contrib import messages

def registro_farmacia_view(request):
    if request.method == 'POST':
        form = RegistroFarmaciaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Farmacia registrada correctamente!")
            return redirect('home')
        else:
            # Esto sale en la terminal donde corre runserver
            print("🛑 Errores en registro_farmacia_view:", form.errors.as_json())
            messages.error(request, "Hay errores en el formulario. Revísalos abajo.")
    else:
        form = RegistroFarmaciaForm()
    return render(request, 'accounts/registro_farmacia.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            tipo = user.profile.tipo
            if tipo == 'clinica':
                return redirect('panel_clinica')
            elif tipo == 'farmacia':
                return redirect('panel_farmacia')  # si lo tienes
            else:
                return redirect('home')  # clientes
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from accounts.decorators import tipo_requerido

@login_required
@tipo_requerido('clinica')
def publicar_adopcion(request):
    if request.method == 'POST':
        # aquí va la lógica para procesar el formulario de publicación de adopción
        # por ahora solo un render básico
        pass

    return render(request, 'adopciones/publicar_adopcion.html')

@login_required
@tipo_requerido('clinica')
def panel_clinica(request):
    clinica_user = request.user

    # Reservas solicitadas por clientes (creada_por_clinica=False)
    reservas_pedidas = Reserva.objects.filter(clinica=clinica_user, creada_por_clinica=False).order_by('fecha', 'hora')

    # Reservas realizadas directamente por la clínica (creada_por_clinica=True)
    
    reservas_realizadas = Reserva.objects.filter(clinica=clinica_user, creada_por_clinica=True)

    mascotas = MascotaEnAdopcion.objects.filter(publicada_por=clinica_user)

    return render(request, 'accounts/panel_clinica.html', {
        'mascotas': mascotas,
        'reservas_pedidas': reservas_pedidas,
        'reservas_realizadas': reservas_realizadas,  # 👈 esto es importante
    })

@login_required
@tipo_requerido('farmacia')
def panel_farmacia(request):
    return render(request, 'accounts/panel_farmacia.html')

@login_required
@tipo_requerido('cliente')
def panel_cliente(request):
    return render(request, 'accounts/panel_cliente.html')


@require_POST
@login_required
@tipo_requerido('clinica')
def cambiar_estado_mascota(request):
    mascota_id = request.POST.get('id')
    try:
        mascota = MascotaEnAdopcion.objects.get(id=mascota_id, publicada_por=request.user)
        mascota.estado = 'publicada' if mascota.estado != 'publicada' else 'pendiente'
        mascota.save()
        return JsonResponse({'success': True, 'nuevo_estado': mascota.estado})
    except MascotaEnAdopcion.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

