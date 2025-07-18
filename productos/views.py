from django.shortcuts import render, redirect
from .forms import ProductoForm
from .models import Producto
from django.contrib.auth.decorators import login_required
from accounts.decorators import tipo_requerido
from django.shortcuts import get_object_or_404
from django.contrib import messages
from pedidos.models import Pedido

# Create your views here.

def catalogo_productos(request):
    return render(request, 'productos/catalogo.html')

@login_required
@tipo_requerido('farmacia')
def subir_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.farmacia = request.user
            producto.save()
            return redirect('productos:panel_farmacia')  # o a una vista de lista de productos
    else:
        form = ProductoForm()
    
    return render(request, 'productos/subir_producto.html', {'form': form})

@login_required
@tipo_requerido('farmacia')
def panel_farmacia(request):
    productos = Producto.objects.filter(farmacia=request.user).order_by('-fecha_creacion')

     # Filtrar pedidos que tengan productos de esta farmacia
    pedidos = Pedido.objects.filter(
        items__producto__farmacia=request.user
    ).distinct().prefetch_related('items').select_related('cliente')


    return render(request, 'productos/panel_farmacia.html', {
        'productos': productos,
        'pedidos': pedidos
    })

@login_required
def pedidos_farmacia_view(request):
    # tu lógica aquí
    pedidos = Pedido.objects.filter(farmacia=request.user)

    return render(request, 'productos/pedidos.html', {'pedidos': pedidos})

@login_required
@tipo_requerido('farmacia')
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, farmacia=request.user)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('productos:panel_farmacia')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

@login_required
@tipo_requerido('farmacia')
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, farmacia=request.user)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('panel_farmacia')

    return render(request, 'productos/eliminar_producto.html', {'producto': producto})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

def stock_productos(request):
    productos = Producto.objects.all()  # o filtrar si quieres
    return render(request, 'productos/stock.html', {'productos': productos})

def nuevo_pedido_view(request):
    return render(request, 'productos/nuevo_pedido.html')

def editar_perfil_farmacia(request):
    profile = request.user.profile
    if request.method == 'POST':
        perfil_publicado = request.POST.get('perfil_publicado') == 'on'
        profile.perfil_publicado = perfil_publicado
        profile.save()
        return redirect('productos:pedidos_farmacia')  # O a donde corresponda

    return render(request, 'accounts/editar_perfil_farmacia.html', {'profile': profile})

@login_required
@tipo_requerido('farmacia')
def mis_productos(request):
    productos = Producto.objects.filter(farmacia=request.user).order_by('-fecha_creacion')
    return render(request, 'productos/mis_productos.html', {'productos': productos})

from django.contrib import messages

@login_required
@tipo_requerido('farmacia')
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, farmacia=request.user)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('productos:mis_productos')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})




