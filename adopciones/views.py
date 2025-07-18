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

from .forms import FormularioAdopcion
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
            messages.success(request, "Mascota publicada con éxito.")
            return redirect('panel_clinica') 
        
        else:
            messages.error(request, "Corrige los errores del formulario.")
            print("Errores del formulario:", form.errors)
    else:
        form = MascotaEnAdopcionForm()

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
    
    # Verifica que el usuario sea quien publicó la mascota
    if mascota.publicada_por != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar esta publicación.")
    
    if request.method == 'POST':
        mascota.delete()
        messages.success(request, "Publicación eliminada correctamente.")
        return redirect('adopciones:mis_publicaciones_clinica')  # Cambia 'panel_clinica' por el nombre real de la vista destino
    
    # Si quieres mostrar un confirm dialog, puedes renderizar una plantilla aquí
    # Por ejemplo:
    # return render(request, 'adopciones/confirmar_eliminacion.html', {'mascota': mascota})
    
    # Pero si solo manejas eliminación vía POST (botón), podrías redirigir o mostrar error:
    return redirect('adopciones:mis_publicaciones_clinica')

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
        form = FormularioAdopcion(request.POST)
        if form.is_valid():
            if form.is_valid():
                datos = form.cleaned_data
                solicitud = SolicitudAdopcion.objects.create(
                    nombre_completo=datos['nombre'],
                    email=datos['email'],
                    telefono=datos['telefono'],
                    num_ninos=datos.get('num_ninos'),  # aquí ya puede ser None o un entero válido
                    mascota=mascota,
                    usuario=request.user,
                    # otros campos...
                )

            try:
                solicitud = SolicitudAdopcion.objects.create(
                    nombre_completo=datos['nombre'],
                    email=datos['email'],
                    telefono=datos['telefono'],
                    num_ninos=datos.get('num_ninos'),  # puede ser None si no viene
                    mascota=mascota,
                    usuario=request.user,
                    # Aquí puedes agregar otros campos del formulario cuando los tengas
                )

                mascota.estado = 'en_proceso'  # Asegúrate de que este estado exista en tu modelo
                mascota.save()

                send_mail(
                    subject=f"Solicitud de adopción para {mascota.nombre}",
                    message=(
                        f"Se ha recibido una solicitud de adopción:\n\n"
                        f"Nombre: {datos['nombre']}\n"
                        f"Email: {datos['email']}\n"
                        f"Teléfono: {datos['telefono']}\n\n"
                        f"Revisa los detalles en el panel de administración o en el sistema."
                    ),
                    from_email='no-responder@tusitio.com',
                    recipient_list=[mascota.publicada_por.email],
                    fail_silently=False,
                )
                return redirect('adopcion_solicitud_exitosa')

            except Exception as e:
                print(f"Error al guardar solicitud o enviar correo: {e}")
                error_message = 'Hubo un error al procesar tu solicitud. Inténtalo de nuevo.'
        else:
            error_message = 'Por favor, corrige los errores en el formulario.'
    else:
        form = FormularioAdopcion()
        error_message = None

    return render(request, 'adopciones/formulario_adopcion.html', {
        'mascota': mascota,
        'form': form,
        'error_message': error_message,
    })

@login_required
def procesar_solicitud(request):
    if request.method == "POST":

        mascota_id = request.POST.get("mascota_id")
        mascota = MascotaEnAdopcion.objects.get(id=mascota_id)

        # Convertir valores numéricos
        def parse_int(value):
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

        num_adultos = parse_int(request.POST.get("num_adultos"))
        num_ninos = parse_int(request.POST.get("num_ninos"))

        # Para campos booleanos, también conviene chequear si están en POST
        declaracion_verdadera = request.POST.get("declaracion_verdadera") == 'on'  # o 'true' según tu formulario
        acepto_terminos = request.POST.get("acepto_terminos") == 'on'

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
            num_adultos = num_adultos,
            num_ninos = num_ninos,
            edades_ninos = request.POST.get("edades_ninos"),
            otras_mascotas = request.POST.get("otras_mascotas"),
            tiempo_solo = request.POST.get("tiempo_solo"),
            experiencia_previa = request.POST.get("experiencia_previa"),
            gastos_compromiso = request.POST.get("gastos_compromiso"),
            esterilizacion_compromiso = request.POST.get("esterilizacion_compromiso"),
            planes_futuro = request.POST.get("planes_futuro"),
            declaracion_verdadera = declaracion_verdadera,
            acepto_terminos = acepto_terminos,
            usuario = request.user, 
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
        return redirect('adopciones:solicitud_exitosa') # redirige correctamente con el id # Cambia por el nombre real si usas `name=`
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
        'solicitudes_adopcion': solicitudes_cliente
    })

@login_required
def cancelar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudAdopcion, id=solicitud_id, usuario=request.user)

    if request.method == "POST":
        solicitud.delete()
        messages.success(request, "Solicitud cancelada correctamente.")
        return redirect('adopciones:mis_postulaciones')  # o la URL donde quieras redirigir

    # Si quieres puedes mostrar una confirmación antes de borrar, o redirigir directamente
    return redirect('adopciones:mis_postulaciones')



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
            return redirect('panel_cliente')  # o donde desees llevarlo después
    else:
        form = MascotaAbandonadaForm()

    return render(request, 'adopciones/registrar_mascota_abandonada.html', {'form': form})

@login_required
@tipo_requerido('cliente')
def detalle_reporte_mascota(request, id):
    mascota = get_object_or_404(MascotaAbandonada, id=id, registrada_por=request.user)
    return render(request, 'adopciones/detalle_reporte_mascota_abandonada.html', {'mascota': mascota})

@login_required
@tipo_requerido('cliente')
def editar_reporte_mascota(request, id):
    mascota = get_object_or_404(MascotaAbandonada, id=id, registrada_por=request.user, estado='pendiente')
    if request.method == 'POST':
        form = MascotaAbandonadaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('adopciones:detalle_reporte_mascota', id=mascota.id)
    else:
        form = MascotaAbandonadaForm(instance=mascota)
    return render(request, 'adopciones/editar_reporte_mascota_abandonada.html', {'form': form, 'mascota': mascota})

@login_required
@tipo_requerido('cliente')
def eliminar_reporte_mascota(request, id):
    mascota = get_object_or_404(MascotaAbandonada, id=id, registrada_por=request.user, estado='pendiente')
    if request.method == 'POST':
        mascota.delete()
        return redirect('panel_cliente')
    return render(request, 'adopciones/confirmar_eliminacion_mascota_abandonada.html', {'mascota': mascota})

@login_required
def mis_reportes_mascota_abandonada(request):
    reportes = MascotaAbandonada.objects.filter(registrada_por=request.user).order_by('-fecha_registro')
    return render(request, 'adopciones/mis_reportes_mascota_abandonada.html', {'reportes': reportes})




@login_required
@tipo_requerido('clinica')  # si tienes decorador para tipo usuario
def lista_reportes_pendientes(request):
    reportes = MascotaAbandonada.objects.filter(estado='pendiente').order_by('fecha_registro')
    return render(request, 'adopciones/reportes_pendientes_clinica.html', {'reportes': reportes})


@login_required
@tipo_requerido('clinica')
def revisar_reporte(request, reporte_id):
    reporte = get_object_or_404(MascotaAbandonada, id=reporte_id)
    
    if request.method == 'POST':
        decision = request.POST.get('decision')
        if decision in ['aprobada', 'rechazada']:
            reporte.estado = decision
            if decision == 'aprobada':
                reporte.aprobada_por = request.user
                reporte.fecha_aprobacion = timezone.now()
            else:
                reporte.aprobada_por = None
                reporte.fecha_aprobacion = None
            reporte.save()
            messages.success(request, f'Reporte {decision} correctamente.')
            return redirect('adopciones:lista_reportes_pendientes')
    
    return render(request, 'adopciones/revisar_reporte_clinica.html', {'reporte': reporte})



from django.http import JsonResponse
from ubicacion.models import Ciudad

def cargar_ciudades(request):
    region_id = request.GET.get('region')
    ciudades = Ciudad.objects.filter(region_id=region_id).order_by('nombre').values('id', 'nombre')
    return JsonResponse(list(ciudades), safe=False)






