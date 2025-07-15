from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from pedidos.models import Pedido, ItemPedido
from productos.models import Producto
from pedidos.models import Pedido
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import locale
locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 



@login_required
def panel_farmacia_pedidos(request):
    # Obtener farmacia actual (usuario logueado)
    farmacia_user = request.user

    # Filtrar pedidos que contienen productos de esta farmacia
    pedidos = Pedido.objects.filter(
        items__producto__farmacia=farmacia_user
    ).distinct().prefetch_related(
        Prefetch('items', queryset=ItemPedido.objects.filter(producto__farmacia=farmacia_user))
    )

    return render(request, 'productos/panel_farmacia_pedidos.html', {'pedidos': pedidos})

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items_con_subtotal = []
    total = 0

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        items_con_subtotal.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    context = {
        'items': items_con_subtotal,
        'total': total,
    }
    return render(request, 'pedidos/carrito.html', context)

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    accion = request.GET.get('accion', 'agregar')

    producto_id_str = str(producto_id)
    
    if accion == 'restar':
        if producto_id_str in carrito:
            carrito[producto_id_str] -= 1
            if carrito[producto_id_str] <= 0:
                del carrito[producto_id_str]
    else:  # acción por defecto: agregar
        if producto_id_str in carrito:
            carrito[producto_id_str] += 1
        else:
            carrito[producto_id_str] = 1

    request.session['carrito'] = carrito
    return redirect('pedidos:ver_carrito')

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]

    request.session['carrito'] = carrito
    return redirect('pedidos:ver_carrito')

    return redirect('core:home')

@login_required
def panel_farmacia_pedidos(request):
    # Asumiendo que cada farmacia es un User con profile.tipo == 'farmacia'
    pedidos = Pedido.objects.filter(farmacia=request.user, completado=True).order_by('-creado')

    return render(request, 'farmacias/panel_pedidos.html', {'pedidos': pedidos})

@login_required
def finalizar_pedido(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})

        if not carrito:
            messages.error(request, "Tu carrito está vacío.")
            return redirect('pedidos:ver_carrito')

        # Crear pedido
        pedido = Pedido.objects.create(
            cliente=request.user,
            completado=True,
            estado='pendiente'
        )

        # Crear los items del pedido
        for producto_id, cantidad in carrito.items():
            producto = get_object_or_404(Producto, id=producto_id)
            ItemPedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad
            )

        # Vaciar el carrito
        request.session['carrito'] = {}

        messages.success(request, "¡Tu pedido fue finalizado con éxito!")
        return redirect('pedidos:pedido_confirmado')  # esta será la página de gracias

    return redirect('pedidos:ver_carrito')

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-creado')

    # Agregar un atributo total a cada pedido
    for pedido in pedidos:
        total = 0
        for item in pedido.items.all():
            total += item.cantidad * item.producto.precio
        pedido.total_formateado = f"${total:,.0f}".replace(',', '.')

    context = {
        'pedidos': pedidos,
    }
    return render(request, 'pedidos/mis_pedidos.html', context)

@login_required
def pedido_confirmado(request):
    return render(request, 'pedidos/pedido_confirmado.html')

def listado_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listado.html', {'productos': productos})

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    if pedido.estado not in ['cancelado', 'enviado']:
        pedido.estado = 'cancelado'
        pedido.save()
        messages.success(request, 'Tu pedido ha sido cancelado correctamente.')
    else:
        messages.error(request, 'Este pedido no puede ser cancelado.')
    return redirect('pedidos:mis_pedidos')