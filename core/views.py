from django.shortcuts import render, redirect
from .forms import MascotaForm
from .models import Mascota
from .forms import ClinicaForm
from .models import Clinica
from django.contrib import messages
from .forms import MascotaAdopcionForm
from django.contrib.auth.decorators import login_required
from adopciones.models import MascotaEnAdopcion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile  
from productos.models import Producto
from farmacias.models import Farmacia
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from adopciones.views import lista_mascotas_adopcion
from adopciones.forms import FiltroMascotaForm

import locale


def adopciones(request):
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
        ubicacion = form.cleaned_data.get('ubicacion')

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
        if ubicacion:
            # Busca en el campo 'direccion' de profile que está en publicada_por
            mascotas = mascotas.filter(publicada_por__profile__direccion__icontains=ubicacion)

    return render(request, 'adopciones.html', {
        'form': form,
        'mascotas': mascotas,
    })

def clinicas_view(request):
    if request.method == 'POST':
        form = ClinicaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clínica publicada correctamente.')
            return redirect('clinicas')
    else:
        form = ClinicaForm()

    clinicas = User.objects.filter(profile__tipo='clinica')

    return render(request, 'clinicas.html', {
        'form': form,
        'clinicas': clinicas
    })

def farmacias_view(request):
    farmacias = User.objects.filter(profile__tipo='farmacia', profile__perfil_publicado=True)
    return render(request, 'core/farmacias.html', {'farmacias': farmacias})

def contacto_view(request):
    return render(request, 'contacto.html')

@login_required
def publicar_adopcion(request):
    if request.method == 'POST':
        form = MascotaAdopcionForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.publicado_por = request.user
            mascota.publicado = False  # para que la clínica revise antes de publicar
            mascota.save()
            return redirect('adopciones')  # o a donde quieras
    else:
        form = MascotaAdopcionForm()
    return render(request, 'adopciones/publicar_adopcion.html', {'form': form})

def lista_mascotas_publicas(request):
    mascotas = MascotaEnAdopcion.objects.filter(estado='publicada').order_by('-fecha_publicacion')
    return render(request, 'adopciones/lista_adopciones.html', {'mascotas': mascotas})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # o a donde quieras redirigir
    else:
        form = UserCreationForm()
    return render(request, 'accounts/registro.html', {'form': form})

def home(request):
    mascotas_clinica = MascotaEnAdopcion.objects.filter(
        publicada_por__profile__tipo='clinica',
        estado='publicada'
    )
    clinicas = User.objects.filter(profile__tipo='clinica')

    productos = Producto.objects.filter(estado='publicado') 

    return render(request, 'home.html', {
        'mascotas_clinica': mascotas_clinica,
        'clinicas': clinicas, 
        'productos': productos,
    })

def productos_publicados(request):
    productos = Producto.objects.filter(estado='publicado')

    # Configura la localización para Chile
    # Es crucial que tu sistema tenga este locale instalado.
    # En sistemas Linux/Mac, 'es_CL.UTF-8' es el más común.
    # En Windows, puede ser 'Spanish_Chile.1252' o 'es_CL'.
    # Si no funciona el primero, prueba otros o investiga el nombre exacto para tu OS.
    try:
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') # Opción preferida para Linux/Mac
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'es_CL') # Otra opción para Linux/Mac
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'Spanish_Chile.1252') # Opción común para Windows
            except locale.Error:
                print("Advertencia: No se pudo establecer un locale chileno específico. El formato de moneda podría no ser el esperado.")
                locale.setlocale(locale.LC_ALL, '') # Fallback: usa el locale por defecto del sistema


    productos_con_precio_formateado = []
    for producto in productos:
        # Asegúrate de que producto.precio sea un número (int o float)
        # Si es un objeto Decimal, conviértelo a float para locale.format_string
        try:
            precio_flotante = float(producto.precio)
        except (TypeError, ValueError):
            precio_flotante = 0.0 # Valor por defecto si el precio no es un número válido

        # Formatear el número con separador de miles (punto) y sin decimales
        # %d es para enteros, grouping=True para los separadores de miles
        precio_formateado = locale.format_string("%d", precio_flotante, grouping=True)

        productos_con_precio_formateado.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio, # Mantener el original por si acaso
            'precio_clp': precio_formateado, # Este es el campo que usaremos en la plantilla
            'imagen': producto.imagen,
            'farmacia': producto.farmacia, # Pasar el objeto completo si lo necesitas en la plantilla
            # Asegúrate de pasar también tus campos para data-category en la plantilla
            'es_farmacia': producto.es_farmacia if hasattr(producto, 'es_farmacia') else False,
            'es_veterinaria': producto.es_veterinaria if hasattr(producto, 'es_veterinaria') else False,
            'en_oferta': producto.en_oferta if hasattr(producto, 'en_oferta') else False,
            # ... cualquier otro campo que necesites
        })

    return render(request, 'core/productos_publicados.html', {'productos': productos_con_precio_formateado})

