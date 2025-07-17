from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MascotaForm, TutorForm
from accounts.decorators import tipo_requerido
from accounts.models import Profile
from accounts.forms import PerfilClinicaForm
from clinicas.models import HorarioAtencion, Mascota, HistorialVacuna, Consulta
from clinicas.forms import HorarioAtencionForm, HorarioAtencionFormSet, HistorialVacunaForm, ConsultaForm  # o donde lo tengas
from .serializers import RazaSerializer
from .forms import ConsultaForm
from clinicas.models import Tutor
from django.db.models import Q
from .forms import ServicioForm
from clinicas.models import Servicio
from ubicacion.models import Region, Ciudad

@login_required
@tipo_requerido('clinica')
def editar_horario(request):
    profile = request.user.profile
    horarios = HorarioAtencion.objects.filter(clinica=request.user)

    if request.method == 'POST':
        form = PerfilClinicaForm(request.POST, request.FILES, instance=profile, user=request.user)
        formset = HorarioAtencionFormSet(request.POST, instance=profile)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "✅ Los datos se actualizaron correctamente.")
            return redirect('panel_clinica')
    else:
        form = PerfilClinicaForm(instance=profile, user=request.user)
        formset = HorarioAtencionFormSet(instance=profile)

    return render(request, 'clinicas/editar_horario.html', {
        'form': form,
        'formset': formset,
        'horarios': horarios
    })

@login_required
@tipo_requerido('clinica')
def ficha_clinica(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    consultas = Consulta.objects.filter(mascota=mascota).order_by('-fecha')

    context = {
        'mascota': mascota,
        'consultas': consultas,
    }
    return render(request, 'clinicas/ficha_clinica.html', context)

@login_required
@tipo_requerido('clinica')
def agregar_vacuna(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.method == 'POST':
        form = HistorialVacunaForm(request.POST)
        if form.is_valid():
            vacuna = form.save(commit=False)
            vacuna.mascota = mascota
            vacuna.save()
            return redirect('clinica:ficha_clinica', mascota_id=mascota.id)
    else:
        form = HistorialVacunaForm()

    return render(request, 'clinica/agregar_vacuna.html', {'form': form, 'mascota': mascota})

@login_required
@tipo_requerido('clinica')
def agregar_consulta(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.mascota = mascota
            consulta.save()
            return redirect('clinica:ficha_clinica', mascota_id=mascota.id)
    else:
        form = ConsultaForm()

    return render(request, 'clinica/agregar_consulta.html', {'form': form, 'mascota': mascota})

@login_required
@tipo_requerido('clinica')
def registrar_mascota(request):
    if request.method == 'POST':
        mascota_form = MascotaForm(request.POST)
        tutor_form = TutorForm(request.POST)

        if mascota_form.is_valid() and tutor_form.is_valid():
            nombre_tutor_limpio = tutor_form.cleaned_data.get('nombre') # El campo en tu modelo Tutor es 'nombre'
            email_tutor_limpio = tutor_form.cleaned_data.get('email')
            telefono_tutor_limpio = tutor_form.cleaned_data.get('telefono')

            tutor_existente = Tutor.objects.filter(
                nombre=nombre_tutor_limpio,
                email=email_tutor_limpio,
                telefono=telefono_tutor_limpio
            ).first()

            if tutor_existente:
                tutor = tutor_existente
            else:
                tutor = tutor_form.save()

            mascota = mascota_form.save(commit=False)
            mascota.tutor = tutor
            mascota.clinica = request.user
            mascota.save()

            from django.contrib import messages
            messages.success(request, 'Mascota y Tutor registrados exitosamente.')

            return redirect('panel_clinica')
        else:
            from django.contrib import messages
            messages.error(request, 'Por favor, corrige los errores en los formularios.')

    else: # GET request
        mascota_form = MascotaForm()
        tutor_form = TutorForm()

    return render(request, 'clinicas/registrar_mascota.html', {
        'mascota_form': mascota_form,
        'tutor_form': tutor_form,
    })

def nueva_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinica:panel_clinica')  # o donde quieras redirigir después
    else:
        form = ConsultaForm()
    return render(request, 'clinicas/nueva_consulta.html', {'form': form})

@login_required
@tipo_requerido('clinica') # Asegúrate de que solo los usuarios de clínica puedan acceder a esto
def listado_mascotas(request):
    current_clinic_user = request.user
    query = request.GET.get('q') # Obtiene el término de búsqueda de la URL

    # Primero, filtra las mascotas por la clínica actual
    mascotas = Mascota.objects.filter(clinica=current_clinic_user)

    # Si hay un término de búsqueda, aplica filtros adicionales
    if query:
        mascotas = mascotas.filter(
            # Busca por el nombre de la mascota (nombre_mascota)
            Q(nombre_mascota__icontains=query) |
            # O busca por el nombre del tutor asociado a la mascota
            Q(tutor__nombre_tutor__icontains=query)
        ).distinct() # Usa .distinct() para evitar duplicados si una mascota aparece por múltiples criterios del mismo tutor

    # Ordena las mascotas para una presentación consistente
    mascotas = mascotas.order_by('nombre_mascota')

    context = {
        'mascotas': mascotas,
        'query': query, # Pasa el término de búsqueda a la plantilla para que se mantenga en la barra
        'title': 'Listado de Pacientes',
    }
    return render(request, 'clinicas/listado_mascotas.html', context)
@login_required
@tipo_requerido('clinica')
def ficha_clinica(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    tutor = mascota.tutor
    consultas = Consulta.objects.filter(mascota=mascota).order_by('-fecha')

    # Formulario para tutor y mascota
    if request.method == 'POST':
    

        tutor_form = TutorForm(request.POST, instance=tutor)
        mascota_form = MascotaForm(request.POST, instance=mascota)
        consulta_form = ConsultaForm(request.POST)

        # Si el formulario del tutor/mascota se está guardando
        if 'guardar_tutor_mascota' in request.POST:
            if tutor_form.is_valid() and mascota_form.is_valid():
                

             
                tutor_form.save()
                mascota_form.save()
                return redirect('clinica:ficha_clinica', mascota_id=mascota.id)
            
        elif 'agregar_consulta' in request.POST:
            if consulta_form.is_valid():
                print(consulta_form.cleaned_data)

                consulta = consulta_form.save(commit=False)
                consulta.mascota = mascota
                consulta.clinica = request.user
                consulta.save()
                return redirect('clinica:ficha_clinica', mascota_id=mascota.id)
            else:
                print(consulta_form.errors)

    else: # GET request
        tutor_form = TutorForm(instance=tutor)
        mascota_form = MascotaForm(instance=mascota)
        consulta_form = ConsultaForm()

    return render(request, 'clinicas/ficha_clinica.html', {
        'mascota': mascota,
        'tutor_form': tutor_form,
        'mascota_form': mascota_form,
        'consulta_form': consulta_form,
        'consultas': consultas,
    })

def registrar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinica:listado_servicios')  # O a donde prefieras
    else:
        form = ServicioForm()
    return render(request, 'clinicas/registrar_servicio.html', {'form': form})

def listado_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'clinicas/listado_servicios.html', {'servicios': servicios})

def historial_medico(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Seguridad: el usuario debe ser el tutor o propietario
    if mascota.propietario != request.user and mascota.tutor.usuario != request.user:
        return render(request, 'core/no_autorizado.html')

    consultas = mascota.consultas.all()  # Gracias al related_name='consultas'

    return render(request, 'clinicas/historial_medico.html', {
        'mascota': mascota,
        'consultas': consultas
    })

@login_required
@tipo_requerido('clinica')
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            return redirect('clinicas:ficha_clinica', mascota_id=consulta.mascota.id)
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, 'clinicas/editar_consulta.html', {
        'form': form,
        'consulta': consulta,
    })

@login_required
def mis_mascotas_cliente(request):
    mascotas = Mascota.objects.filter(propietario=request.user)
    return render(request, 'clinicas/mis_mascotas_cliente.html', {'mascotas': mascotas})

def buscar_clinicas(request):
    regiones = Region.objects.all().order_by('nombre')
    ciudades = Ciudad.objects.none()  # Por defecto vacío

    region_id = request.GET.get('region')
    ciudad_id = request.GET.get('ciudad')

    clinicas = Profile.objects.filter(tipo='clinica', perfil_publicado=True)

    if region_id:
        clinicas = clinicas.filter(region_id=region_id)
        ciudades = Ciudad.objects.filter(region_id=region_id).order_by('nombre')
    
    if ciudad_id:
        clinicas = clinicas.filter(ciudad_id=ciudad_id)

    context = {
        'regiones': regiones,
        'ciudades': ciudades,
        'clinicas': clinicas,
        'region_id': region_id,
        'ciudad_id': ciudad_id,
    }

    return render(request, 'clinicas/buscar_clinicas.html', context)


