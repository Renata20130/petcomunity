from django.shortcuts import render
from django.contrib.auth.models import User
from ubicacion.models import Region, Ciudad
from farmacias.models import Farmacia

# Create your views here.
from django.shortcuts import render
from .models import Farmacia

def lista_farmacias_con_productos(request):
    # Filtra solo usuarios que sean farmacias. Asumo que tienes perfil con tipo:
    farmacias = User.objects.filter(profile__tipo='farmacia').prefetch_related('productos')

    context = {
        'farmacias': farmacias,
    }
    return render(request, 'farmacias/lista_farmacias.html', context)

def buscar_farmacias(request):
    region_id = request.GET.get('region')
    ciudad_id = request.GET.get('ciudad')

    regiones = Region.objects.all()
    ciudades = Ciudad.objects.none()
    farmacias = Farmacia.objects.none()

    if region_id:
        ciudades = Ciudad.objects.filter(region_id=region_id)
    if ciudad_id:
        farmacias = Farmacia.objects.filter(ciudad_id=ciudad_id)
    elif region_id:
        farmacias = Farmacia.objects.filter(ciudad__region_id=region_id)

    return render(request, 'farmacias/buscar_farmacias.html', {
        'regiones': regiones,
        'ciudades': ciudades,
        'farmacias': farmacias,
        'region_id': region_id,
        'ciudad_id': ciudad_id,
    })





