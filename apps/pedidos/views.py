from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView

from .decorators import get_carrito_and_pedido


class PedidosListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'pedidos/pedidos.html'
    context_object_name = 'lista_pedidos'

    def get_queryset(self): 
        return self.request.user.pedidos()


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def pedido(request, pedido):
    if not pedido.carrito.productos.exists():
        return redirect('carts:cart')

    return render(request, 'pedidos/pedido.html', {
        'carrito': pedido.carrito,
        'pedido': pedido,
    })
