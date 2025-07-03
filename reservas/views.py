from django.shortcuts import render, redirect
from .forms import ReservaForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import tipo_requerido

@login_required
def agendar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user
            reserva.save()
            return redirect('home')  # o donde quieras redirigir
    else:
        form = ReservaForm()
    
    return render(request, 'reservas/agendar_reserva.html', {'form': form})

@login_required
@tipo_requerido('clinica')
def registrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.clinica = request.user
            reserva.creada_por_clinica = True  # ¡funcionará porque ya existe ese campo!
            reserva.save()
    else:
        form = ReservaForm()
    return render(request, 'reservas/registrar_reserva.html', {'form': form})