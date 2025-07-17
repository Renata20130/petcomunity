from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import tipo_requerido
from django.views.decorators.csrf import csrf_protect

from .forms import MascotaEnAdopcionForm
from .models import MascotaEnAdopcion
from .models import SolicitudAdopcion

from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from accounts.models import Profile  
from django.contrib.auth.models import User

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone


from .forms import FiltroMascotaForm
from .forms import MascotaAbandonadaForm
from .models import MascotaAbandonada

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
    
    # Esta línea es CLAVE para la depuración
    print("Campos del form en la vista:", form.fields)
    
    return render(request, 'adopciones/publicar_adopcion.html', {'form': form})

@login_required
@tipo_requerido('clinica')
def panel_clinica(request):
    mascotas = MascotaEnAdopcion.objects.filter(publicada_por=request.user)
    
    # Obtener las solicitudes de adopción asociadas a esas mascotas
    solicitudes = SolicitudAdopcion.objects.filter(mascota__in=mascotas).order_by('-fecha_envio')

    return render(request, 'accounts/panel_clinica.html', {
        'mascotas': mascotas,
        'solicitudes': solicitudes,
    })

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

@require_POST
def actualizar_estado_mascota(request, mascota_id):
    try:
        mascota = MascotaEnAdopcion.objects.get(id=mascota_id)
    except MascotaEnAdopcion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mascota no encontrada'}, status=404)

    try:
        data = json.loads(request.body)
        nuevo_estado = data.get('estado')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)

    if nuevo_estado in ['publicada', 'pendiente', 'adoptada']: # Ajusta los estados según tu modelo
        mascota.estado = nuevo_estado
        mascota.save()
        return JsonResponse({'success': True, 'estado_actual': mascota.estado})
    else:
        return JsonResponse({'success': False, 'error': 'Estado inválido'}, status=400)

@login_required
def formulario_adopcion_view(request, mascota_id):
    mascota = get_object_or_404(MascotaEnAdopcion, id=mascota_id)

    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        # Agrega todos los demás campos aquí...
        
        if not nombre_completo or not email or not telefono:
            return render(request, 'adopciones/formulario_adopcion.html', {
                'mascota': mascota,
                'error_message': 'Por favor, completa todos los campos obligatorios.'
            })

        try:
            solicitud = SolicitudAdopcion.objects.create(
                nombre_completo=nombre_completo,
                email=email,
                telefono=telefono,
                mascota=mascota,
                usuario=request.user  # si tienes un campo ForeignKey en SolicitudAdopcion

            )

            # Cambiar el estado de la mascota a "en proceso" (si lo usas)
            mascota.estado = 'en_proceso'  # Asegúrate de que esté en tus choices si usas eso
            mascota.save()

            # Enviar correo a la clínica que publicó la mascota
            send_mail(
                subject=f"Solicitud de adopción para {mascota.nombre}",
                message=(
                    f"Se ha recibido una solicitud de adopción:\n\n"
                    f"Nombre: {nombre_completo}\n"
                    f"Email: {email}\n"
                    f"Teléfono: {telefono}\n\n"
                    f"Revisa los detalles en el panel de administración o en el sistema."
                ),
                from_email='no-responder@tusitio.com',
                recipient_list=[mascota.publicada_por.email],
                fail_silently=False
            )

        except Exception as e:
            print(f"Error al guardar solicitud o enviar correo: {e}")
            return render(request, 'adopciones/formulario_adopcion.html', {
                'mascota': mascota,
                'error_message': 'Hubo un error al procesar tu solicitud. Inténtalo de nuevo.'
            })

        return redirect('adopcion_solicitud_exitosa')

    # GET (cuando se carga el formulario)
    return render(request, 'adopciones/formulario_adopcion.html', {
        'mascota': mascota
    })

@login_required
def procesar_solicitud(request):
    if request.method == "POST":

        mascota_id = request.POST.get("mascota_id")
        mascota = MascotaEnAdopcion.objects.get(id=mascota_id)

        solicitud = SolicitudAdopcion(
            mascota=mascota,
            nombre_completo = request.POST.get("nombre_completo"),
            dni = request.POST.get("dni"),
            fecha_nacimiento = request.POST.get("fecha_nacimiento"),
            email = request.POST.get("email"),
            telefono = request.POST.get("telefono"),
            direccion = request.POST.get("direccion"),
            tipo_vivienda = request.POST.get("tipo_vivienda"),
            situacion_vivienda = request.POST.get("situacion_vivienda"),
            permiso_arrendador = request.POST.get("permiso_arrendador"),
            num_adultos = request.POST.get("num_adultos"),
            num_ninos = request.POST.get("num_ninos"),
            edades_ninos = request.POST.get("edades_ninos"),
            otras_mascotas = request.POST.get("otras_mascotas"),
            tiempo_solo = request.POST.get("tiempo_solo"),
            experiencia_previa = request.POST.get("experiencia_previa"),
            gastos_compromiso = request.POST.get("gastos_compromiso"),
            esterilizacion_compromiso = request.POST.get("esterilizacion_compromiso"),
            planes_futuro = request.POST.get("planes_futuro"),
            declaracion_verdadera = bool(request.POST.get("declaracion_verdadera")),
            acepto_terminos = bool(request.POST.get("acepto_terminos")),
            
        )
        solicitud.save()

        send_mail(
            subject=f"Nueva solicitud de adopción para {mascota.nombre}",
            message=(
                f"Se ha recibido una nueva solicitud de adopción.\n\n"
                f"Nombre: {solicitud.nombre_completo}\n"
                f"Email: {solicitud.email}\n"
                f"Teléfono: {solicitud.telefono}\n"
                f"Revisa el sistema para más detalles."
            ),
            from_email="no-reply@tusitio.com",
            recipient_list=[mascota.publicada_por.email],
            fail_silently=False,
        )

 
        messages.success(request, "Haz enviado correctamente la solicitud.")
        return redirect('solicitud_exitosa') # redirige correctamente con el id # Cambia por el nombre real si usas `name=`
    else:
        return redirect('inicio') 

@login_required  
def solicitud_exitosa(request):
    return render(request, 'adopciones/solicitud_exitosa.html')

@login_required
def panel_solicitudes(request):
    usuario = request.user
    mascotas_usuario = MascotaEnAdopcion.objects.filter(publicada_por=usuario)
    solicitudes = SolicitudAdopcion.objects.filter(mascota__in=mascotas_usuario).order_by('-fecha_envio')
    return render(request, 'adopciones/panel_solicitudes.html', {
        'solicitudes': solicitudes,
    })

@login_required
@tipo_requerido('clinica')  # Asegura que solo clínicas accedan
def detalle_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudAdopcion, id=solicitud_id)

    # Seguridad: solo puede verla la clínica que publicó la mascota
    if solicitud.mascota.publicada_por != request.user:
        return render(request, "403.html")  # O redirige a home con error

    return render(request, "adopciones/detalle_solicitud.html", {"solicitud": solicitud})

@login_required
@tipo_requerido('clinica')
def actualizar_estado_solicitud(request, solicitud_id):
    if request.method == 'POST':
        solicitud = get_object_or_404(SolicitudAdopcion, id=solicitud_id)
        nuevo_estado = request.POST.get('estado')

        if nuevo_estado in dict(SolicitudAdopcion.ESTADOS_SOLICITUD).keys():
            solicitud.estado = nuevo_estado
            if nuevo_estado == 'contactado':
                solicitud.fecha_contacto = timezone.now()
            elif nuevo_estado == 'rechazada':
                solicitud.fecha_rechazo = timezone.now()
            else:
                # Si cambia a otro estado, opcionalmente limpia las fechas
                solicitud.fecha_contacto = None
                solicitud.fecha_rechazo = None

            solicitud.save()

            asunto = f"Actualización sobre tu solicitud de adopción: {nuevo_estado.capitalize()}"
            mensaje = f"Hola {solicitud.nombre_completo},\n\n" \
                      f"Tu solicitud para adoptar a {solicitud.mascota.nombre} ha cambiado de estado a '{nuevo_estado}'.\n\n" \
                      "La clínica se pondrá en contacto contigo si es necesario.\n\nGracias por tu interés."
            destinatario = [solicitud.email]

            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                destinatario,
                fail_silently=False,
            )

        return redirect('panel_solicitudes')
    else:
        return redirect('panel_solicitudes')
    
@login_required
def mis_postulaciones(request):
    solicitudes_cliente = SolicitudAdopcion.objects.filter(usuario=request.user)
    return render(request, 'adopciones/mis_postulaciones.html', {
        'solicitudes': solicitudes_cliente
    })

def lista_mascotas_adopcion(request):
    form = FiltroMascotaForm(request.GET or None)
    mascotas = MascotaEnAdopcion.objects.filter(
        publicada_por__profile__tipo='clinica',
        estado='publicada'
    ).order_by('-fecha_publicacion')

    filtro_especie = None

    if form.is_valid():
        especie = form.cleaned_data.get('especie')
        sexo = form.cleaned_data.get('sexo')
        edad_min = form.cleaned_data.get('edad_min')
        edad_max = form.cleaned_data.get('edad_max')
        unidad_edad = form.cleaned_data.get('unidad_edad')
        region = form.cleaned_data.get('region')
        ciudad = form.cleaned_data.get('ciudad')
        
        if especie:
            mascotas = mascotas.filter(especie=especie)
        if sexo:
            mascotas = mascotas.filter(sexo=sexo)
        if edad_min is not None:
            mascotas = mascotas.filter(edad__gte=edad_min)
        if edad_max is not None:
            mascotas = mascotas.filter(edad__lte=edad_max)
        if unidad_edad:
            mascotas = mascotas.filter(unidad_edad=unidad_edad)
        if region:
            mascotas = mascotas.filter(publicada_por__profile__region=region)
        if ciudad:
            mascotas = mascotas.filter(publicada_por__profile__ciudad=ciudad)
            
    context = {
        'form': form,
        'mascotas': mascotas,
    }
    return render(request, 'adopciones/lista_mascotas.html', context)

@login_required
def registrar_mascota_abandonada(request):
    if request.user.profile.tipo != 'cliente':
        return redirect('home')  # o mostrar un error

    if request.method == 'POST':
        form = MascotaAbandonadaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.registrada_por = request.user
            mascota.save()
            return redirect('mis_mascotas_abandonadas')  # redirige donde quieras
    else:
        form = MascotaAbandonadaForm()

    return render(request, 'adopciones/registrar_mascota_abandonada.html', {'form': form})

@login_required
def panel_revision_mascotas(request):
    if request.user.profile.tipo != 'clinica':
        return redirect('home')  # O mostrar mensaje de error

    mascotas_pendientes = MascotaAbandonada.objects.filter(estado='pendiente')

    return render(request, 'adopciones/panel_revision.html', {
        'mascotas': mascotas_pendientes
    })

@login_required
def aprobar_mascota(request, mascota_id):
    mascota = get_object_or_404(MascotaAbandonada, id=mascota_id)
    if request.user.profile.tipo != 'clinica':
        return redirect('home')

    mascota.estado = 'aprobada'
    mascota.aprobada_por = request.user
    mascota.fecha_aprobacion = timezone.now()
    mascota.save()
    return redirect('adopciones:panel_revision')

@login_required
def rechazar_mascota(request, mascota_id):
    mascota = get_object_or_404(MascotaAbandonada, id=mascota_id)
    if request.user.profile.tipo != 'clinica':
        return redirect('home')

    mascota.estado = 'rechazada'
    mascota.aprobada_por = request.user
    mascota.fecha_aprobacion = timezone.now()
    mascota.save()
    return redirect('adopciones:panel_revision')

def lista_mascotas_adopcion(request):
    mascotas = MascotaAbandonada.objects.filter(
        estado='aprobada',
        adoptada=False
    ).order_by('-fecha_aprobacion')

    return render(request, 'adopciones/lista_mascotas.html', {
        'mascotas': mascotas
    })

@login_required
def registrar_mascota_abandonada(request):
    if request.method == 'POST':
        form = MascotaAbandonadaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.registrada_por = request.user
            mascota.save()
            return redirect('cliente:panel_cliente')  # o donde desees llevarlo después
    else:
        form = MascotaAbandonadaForm()

    return render(request, 'adopciones/registrar_mascota_abandonada.html', {'form': form})




