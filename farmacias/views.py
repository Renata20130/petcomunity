from django.shortcuts import render
from django.contrib.auth.models import User
from ubicacion.models import Region, Ciudad
from farmacias.models import Farmacia
from accounts.models import Profile
# Create your views here.
from django.shortcuts import render


def lista_farmacias_con_productos(request):
    # Filtra solo usuarios que sean farmacias. Asumo que tienes perfil con tipo:
    farmacias = Profile.objects.filter(tipo='farmacia', perfil_publicado=True)
    context = {
        'farmacias': farmacias,
    }
    return render(request, 'farmacias/lista_farmacias.html', context)

def buscar_farmacias(request):
    region_id = request.GET.get('region')
    ciudad_id = request.GET.get('ciudad')

    regiones = Region.objects.all()
    ciudades = Ciudad.objects.none()  # vacío al inicio
    farmacias = Profile.objects.filter(tipo='farmacia', perfil_publicado=True)  # todas al inicio

    if region_id:
        ciudades = Ciudad.objects.filter(region_id=region_id)
        farmacias = farmacias.filter(ciudad__region_id=region_id)

    if ciudad_id:
        farmacias = farmacias.filter(ciudad_id=ciudad_id)

    context = {
        'regiones': regiones,
        'ciudades': ciudades,
        'farmacias': farmacias,
        'region_id': region_id,
        'ciudad_id': ciudad_id,
    }
    return render(request, 'farmacias/buscar_farmacias.html', context)

