from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from pedidos.models import Pedido, ItemPedido
from productos.models import Producto

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

