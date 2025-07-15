from django.shortcuts import render
from django.http import JsonResponse
from .models import Ciudad

def ciudades_por_region(request):
    region_id = request.GET.get('region_id')
    ciudades = []
    if region_id:
        ciudades = list(Ciudad.objects.filter(region_id=region_id).values('id', 'nombre'))
    return JsonResponse(ciudades, safe=False)

def api_ciudades(request):
    region_id = request.GET.get('region_id')
    if region_id:
        ciudades = Ciudad.objects.filter(region_id=region_id).order_by('nombre')
        data = [{'id': ciudad.id, 'nombre': ciudad.nombre} for ciudad in ciudades]
    else:
        data = []
    return JsonResponse(data, safe=False)

def cargar_ciudades(request):
    region_id = request.GET.get('region_id')
    if region_id:
        ciudades = Ciudad.objects.filter(region_id=region_id).order_by('nombre')
    else:
        ciudades = Ciudad.objects.none()
    ciudades_list = [{'id': c.id, 'nombre': c.nombre} for c in ciudades]
    return JsonResponse({'ciudades': ciudades_list})