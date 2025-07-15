from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MascotaForm
from accounts.decorators import tipo_requerido
from accounts.models import Profile
from accounts.forms import PerfilClinicaForm
from clinicas.models import HorarioAtencion, Mascota, HistorialVacuna, Consulta
from clinicas.forms import HorarioAtencionForm, HorarioAtencionFormSet, HistorialVacunaForm, ConsultaForm  # o donde lo tengas
from .serializers import RazaSerializer
from .forms import ConsultaForm


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
    vacunas = HistorialVacuna.objects.filter(mascota=mascota).order_by('-fecha_aplicacion')
    consultas = Consulta.objects.filter(mascota=mascota).order_by('-fecha')

    return render(request, 'clinica/ficha_clinica.html', {
        'mascota': mascota,
        'vacunas': vacunas,
        'consultas': consultas
    })

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
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.clinica = request.user  # asigna automáticamente la clínica
            mascota.save()
            return redirect('panel_clinica')  # o donde quieras
    else:
        form = MascotaForm()

    return render(request, 'clinicas/registrar_mascota.html', {'form': form})



def nueva_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clinica:panel_clinica')  # o donde quieras redirigir después
    else:
        form = ConsultaForm()
    return render(request, 'clinicas/nueva_consulta.html', {'form': form})





