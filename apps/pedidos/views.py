from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .decorators import get_carrito_and_pedido

@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def pedido(request, pedido):
    if not pedido.carrito.productos.exists():
        return redirect('carts:cart')

    return render(request, 'pedidos/pedido.html', {
        'carrito': pedido.carrito,
        'pedido': pedido,
    })
