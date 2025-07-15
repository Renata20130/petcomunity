from django.core.management.base import BaseCommand
from ubicacion.models import Region, Ciudad

class Command(BaseCommand):
    help = 'Carga regiones y ciudades principales de Chile'

    def handle(self, *args, **kwargs):
        regiones_ciudades = {
            'Región de Arica y Parinacota': ['Arica', 'Putre'],
            'Región de Tarapacá': ['Iquique', 'Alto Hospicio'],
            'Región de Antofagasta': ['Antofagasta', 'Calama', 'Tocopilla'],
            'Región de Atacama': ['Copiapó', 'Vallenar'],
            'Región de Coquimbo': ['La Serena', 'Coquimbo', 'Ovalle'],
            'Región de Valparaíso': ['Valparaíso', 'Viña del Mar', 'Quilpué', 'San Antonio'],
            'Región Metropolitana de Santiago': ['Santiago', 'Puente Alto', 'Maipú', 'La Florida', 'Las Condes'],
            'Región del Libertador General Bernardo O’Higgins': ['Rancagua', 'San Fernando'],
            'Región del Maule': ['Talca', 'Curicó', 'Linares'],
            'Región de Ñuble': ['Chillán', 'Quirihue'],
            'Región del Biobío': ['Concepción', 'Los Ángeles', 'Talcahuano'],
            'Región de La Araucanía': ['Temuco', 'Angol', 'Villarrica'],
            'Región de Los Ríos': ['Valdivia', 'La Unión'],
            'Región de Los Lagos': ['Puerto Montt', 'Osorno', 'Castro'],
            'Región de Aysén del General Carlos Ibáñez del Campo': ['Coyhaique', 'Puerto Aysén'],
            'Región de Magallanes y de la Antártica Chilena': ['Punta Arenas', 'Puerto Natales']
        }

        for nombre_region, ciudades in regiones_ciudades.items():
            region_obj, created = Region.objects.get_or_create(nombre=nombre_region)
            for ciudad_nombre in ciudades:
                ciudad_obj, created = Ciudad.objects.get_or_create(region=region_obj, nombre=ciudad_nombre)

        self.stdout.write(self.style.SUCCESS('Regiones y ciudades cargadas correctamente.'))
