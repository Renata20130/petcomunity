from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from pedidos.models import Pedido, ItemPedido
from productos.models import Producto
from pedidos.models import Pedido
from django.shortcuts import render, get_object_or_404, redirect

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
    # Obtener el pedido incompleto del usuario
    pedido = Pedido.objects.filter(cliente=request.user, completado=False).first()
    if pedido:
        pedido.completado = True
        pedido.estado = 'pendiente'  # o 'procesando' según tu flujo
        pedido.save()
    return redirect('pedidos:ver_carrito')  # o a la página que desees


@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-creado')
    return render(request, 'pedidos/mis_pedidos.html', {'pedidos': pedidos})


