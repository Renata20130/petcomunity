from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import tipo_requerido
from accounts.models import Profile
from accounts.forms import PerfilClinicaForm
from clinicas.models import HorarioAtencion
from clinicas.forms import HorarioAtencionForm, HorarioAtencionFormSet  # o donde lo tengas

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
        'horarios': horarios
    })
