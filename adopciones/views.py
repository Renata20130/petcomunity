from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from adopciones.forms import MascotaEnAdopcionForm
from accounts.decorators import tipo_requerido
from .models import MascotaEnAdopcion
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.shortcuts import render
from accounts.models import Profile  
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST



def adopciones(request):
    especie = request.GET.get('especie')  # obtiene lo que viene en ?especie=
    mascotas = MascotaEnAdopcion.objects.filter(estado='publicada')

    if especie in ['perro', 'gato', 'otro']:
        mascotas = mascotas.filter(especie=especie)

    return render(request, 'adopciones/adopciones.html', {
        'mascotas': mascotas,
        'filtro_especie': especie
    })

@login_required
@tipo_requerido('clinica')
def publicar_adopcion(request):
    
    if request.method == 'POST':
        form = MascotaEnAdopcionForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.publicada_por = request.user
            
            mascota.save()
            return redirect('panel_clinica')
    else:
        form = MascotaEnAdopcionForm()
    print("Campos del form:", form.fields)  # 👈 AÑADE ESTO   
    return render(request, 'adopciones/publicar_adopcion.html', {'form': form})

@login_required
@tipo_requerido('clinica')
def panel_clinica(request):
    mascotas = MascotaEnAdopcion.objects.filter(publicada_por=request.user)
    return render(request, 'accounts/panel_clinica.html', {'mascotas': mascotas})


@login_required
@tipo_requerido('clinica')
def editar_adopcion(request, mascota_id):
    mascota = get_object_or_404(MascotaEnAdopcion, id=mascota_id, publicada_por=request.user)

    if request.method == 'POST':
        form = MascotaEnAdopcionForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('panel_clinica')
    else:
        form = MascotaEnAdopcionForm(instance=mascota)

    return render(request, 'adopciones/editar_adopcion.html', {'form': form, 'mascota': mascota})

@login_required
@tipo_requerido('clinica')
def eliminar_adopcion(request, pk):
    mascota = get_object_or_404(MascotaEnAdopcion, pk=pk)
    if mascota.publicada_por != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar esta publicación.")
    if request.method == 'POST':
        mascota.delete()
        return redirect('panel_clinica')

def lista_mascotas_publicas(request):
    mascotas = MascotaEnAdopcion.objects.filter(estado='publicada')
    return render(request, 'adopciones/lista_publica.html', {'mascotas': mascotas})


def detalle_mascota(request, mascota_id):
    mascota = MascotaEnAdopcion.objects.get(id=mascota_id)
    es_duenio = request.user.is_authenticated and mascota.publicada_por == request.user
    form = MascotaEnAdopcionForm(instance=mascota)

    if request.method == 'POST':
        form = MascotaEnAdopcionForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('panel_clinica')

    return render(request, 'adopciones/editar_desde_detalle.html', {
        'form': form,
        'mascota': mascota
    })


@login_required
@tipo_requerido('clinica')
@require_POST # Asegura que solo acepte solicitudes POST
def cambiar_estado_mascota(request):
    try:
        data = json.loads(request.body) # Parsea el JSON del cuerpo de la solicitud
        mascota_id = data.get('mascota_id')
        nuevo_estado = data.get('estado') # 'publicada' o 'pendiente'

        mascota = get_object_or_404(MascotaEnAdopcion, id=mascota_id, publicada_por=request.user)

        # Validación básica del estado (opcional, pero buena práctica)
        if nuevo_estado not in ['publicada', 'pendiente']:
            return JsonResponse({'success': False, 'message': 'Estado inválido.'}, status=400)

        mascota.estado = nuevo_estado
        mascota.save()

        return JsonResponse({'success': True, 'message': 'Estado actualizado.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Solicitud JSON inválida.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    

@login_required
@tipo_requerido('clinica')
def mis_publicaciones_clinica(request):
    mascotas = MascotaEnAdopcion.objects.filter(publicada_por=request.user)
    context = {
        'mascotas': mascotas,
        'is_dedicated_page': True # Una bandera para posibles usos futuros en la plantilla
    }
    return render(request, 'adopciones/mis_publicaciones_clinica.html', context)

