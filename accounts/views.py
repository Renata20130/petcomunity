from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from adopciones.models import MascotaEnAdopcion, SolicitudAdopcion
from accounts.models import Profile

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

from accounts.decorators import tipo_requerido

from reservas.models import Reserva
from productos.models import Producto
from django.contrib.auth.models import User

from accounts.forms import EditarPerfilClinicaForm
from clinicas.models import HorarioAtencion
from clinicas.forms import HorarioAtencionFormSet
from clinicas.forms import HorarioAtencionForm

from django.forms import modelformset_factory
from pedidos.models import Pedido
from productos.forms import ProductoForm

from adopciones.models import SolicitudAdopcion

from .forms import RegistroForm, RegistroClinicaForm, RegistroFarmaciaForm  # Crearemos estos formularios separados

from .forms import EditarPerfilForm, EditarPerfilExtendidoForm
from .forms import EditarPerfilFarmaciaForm

from itertools import chain
from clinicas.models import Mascota

from .forms import FiltroUbicacionForm

from django.contrib.auth.views import LoginView

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
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
            return redirect('core:home')
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
            return redirect('core:home')
    else:
        form = RegistroClinicaForm()
    return render(request, 'accounts/registro_clinica.html', {'form': form})

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
    next_url = request.GET.get('next', '') or request.POST.get('next', '')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirigir a 'next' si existe, sino a home según tipo
            if next_url:
                return redirect(next_url)
            
            tipo = user.profile.tipo
            if tipo == 'clinica':
                return redirect('core:home')
            elif tipo == 'farmacia':
                return redirect('core:home')
            else:
                return redirect('core:home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {
        'form': form,
        'next': next_url,  # para el input hidden en el form
    })


def logout_view(request):
    logout(request)
    return redirect('core:home')

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
    print("✅ VISTA panel_clinica EJECUTADA")
    clinica_user = request.user
    print("Usuario autenticado:", clinica_user.username)

    reservas = Reserva.objects.filter(clinica=clinica_user, creada_por_clinica=False).order_by('fecha', 'hora')
    print("Reservas encontradas:", reservas.count())

    mascotas = MascotaEnAdopcion.objects.filter(publicada_por=clinica_user)
    solicitudes = SolicitudAdopcion.objects.filter(mascota__in=mascotas).order_by('-fecha_envio')

    mascotas_clinica = Mascota.objects.filter(clinica=clinica_user)

    return render(request, 'accounts/panel_clinica.html', {
        'mascotas': mascotas,
        'mascotas_clinica': mascotas_clinica,
        'reservas': reservas,  # Paso solo estas reservas al template
        'solicitudes': solicitudes,
    })

@login_required
@tipo_requerido('farmacia')
def panel_farmacia(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.farmacia = request.user
            producto.save()
            # Puedes agregar un mensaje de éxito aquí
    else:
        form = ProductoForm()

    productos = Producto.objects.filter(farmacia=request.user)

    return render(request, 'accounts/panel_farmacia.html', {
        'form': form,
        'productos': productos,
    })

@login_required
@tipo_requerido('cliente')
def panel_cliente(request):
    usuario = request.user  # 👈 Agregado

    productos = Producto.objects.all()
    mascotas = MascotaEnAdopcion.objects.filter(estado='publicada')
    clinicas = User.objects.filter(profile__tipo='clinica')

    reservas = Reserva.objects.filter(cliente=usuario).order_by('-fecha', '-hora')
    pedidos = Pedido.objects.filter(cliente=usuario).order_by('-creado')

    solicitudes_adopcion = SolicitudAdopcion.objects.filter(email=request.user.email).order_by('-fecha_envio')


    return render(request, 'accounts/panel_cliente.html', {
        'productos': productos,
        'mascotas': mascotas,
        'clinicas': clinicas,
        'reservas': reservas,
        'pedidos': pedidos,
        'solicitudes_adopcion': solicitudes_adopcion,  # 👈 Pasado al template
    })

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

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('panel_cliente')

    return render(request, 'accounts/editar_perfil.html')

@login_required
def editar_perfil_clinica(request):
    profile = request.user.profile

    if profile.tipo != 'clinica':
        return redirect('home')

    HorarioAtencionFormSet = modelformset_factory(HorarioAtencion, form=HorarioAtencionForm, can_delete=True, extra=1)

    if request.method == 'POST':
        form = EditarPerfilClinicaForm(request.POST, request.FILES, instance=profile, user=request.user)
        formset = HorarioAtencionFormSet(request.POST, queryset=profile.horarios.all())
        
        if form.is_valid() and formset.is_valid():
            form.save()
            horarios = formset.save(commit=False)
            for horario in horarios:
                horario.profile = profile
                horario.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, "✅ Los datos se actualizaron correctamente.")
            return redirect('panel_clinica')
        else:
            messages.error(request, "❌ Hay errores en el formulario, por favor revisa los datos.")

    else:
        form = EditarPerfilClinicaForm(instance=profile, user=request.user)
        formset = HorarioAtencionFormSet(queryset=profile.horarios.all())

    return render(request, 'accounts/editar_perfil_clinica.html', {
        'form': form,
        'formset': formset
    })

def panel_reservas_clinica(request):
    # Aquí consultas las reservas de la clínica y las pasas al template
    reservas = request.user.reservas_recibidas.all()  # asumiendo relación con User
    return render(request, 'reservas/panel_reservas_clinica.html', {'reservas': reservas})

@login_required
def panel_farmacia_pedidos(request):
    # Solo permitir acceso a usuarios tipo farmacia
    if not request.user.profile.tipo == 'farmacia':
        # Puedes redirigir o mostrar error
        return render(request, 'accounts/no_autorizado.html')

    pedidos = Pedido.objects.filter(farmacia=request.user, completado=True).order_by('-creado')

    return render(request, 'accounts/panel_farmacia_pedidos.html', {'pedidos': pedidos})
    
@login_required
def editar_perfil_cliente(request):
    user = request.user
    if request.method == 'POST':
        form_user = EditarPerfilForm(request.POST, instance=user)
        form_profile = EditarPerfilExtendidoForm(request.POST, request.FILES, instance=user.profile)
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            return redirect('panel_cliente')  # redirige al panel
    else:
        form_user = EditarPerfilForm(instance=user)
        form_profile = EditarPerfilExtendidoForm(instance=user.profile)

    return render(request, 'accounts/editar_perfil_cliente.html', {
        'form_user': form_user,
        'form_profile': form_profile,
    })

@login_required
def editar_perfil_farmacia(request):
    profile = request.user.profile

    if profile.tipo != 'farmacia':
        messages.error(request, "No tienes permiso para editar este perfil.")
        return redirect('home')

    if request.method == 'POST':
        form = EditarPerfilFarmaciaForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('productos:pedidos_farmacia')
    else:
        form = EditarPerfilFarmaciaForm(instance=profile, user=request.user)  # <--- Aquí pasas user

    return render(request, 'accounts/editar_perfil_farmacia.html', {
        'form': form
    })

def buscar_clinicas_farmacias(request):
    form = FiltroUbicacionForm(request.GET or None)

    clinicas = Profile.objects.filter(tipo='clinica', perfil_publicado=True)
    farmacias = Profile.objects.filter(tipo='farmacia', perfil_publicado=True)

    if form.is_valid():
        region = form.cleaned_data.get('region')
        ciudad = form.cleaned_data.get('ciudad')

        if region:
            clinicas = clinicas.filter(region=region)
            farmacias = farmacias.filter(region=region)
        if ciudad:
            clinicas = clinicas.filter(ciudad=ciudad)
            farmacias = farmacias.filter(ciudad=ciudad)

    context = {
        'form': form,
        'clinicas': clinicas,
        'farmacias': farmacias,
    }
    return render(request, 'buscar_ubicacion.html', context)

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        # Si tiene perfil
        if hasattr(user, 'profile'):
            if user.profile.tipo == 'cliente':
                # Si es cliente, redirige a donde quería ir o a 'pedir_cita'
                return self.get_redirect_url() or '/reservas/pedir-cita/'
            else:
                # Si es clínica o farmacia, redirige al home
                return '/'
        # Por si no tiene perfil
        return '/'



