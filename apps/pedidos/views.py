from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView

from .decorators import get_carrito_and_pedido
from .utils import breadcrumb

from apps.direcciones.models import Direccion


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
        return redirect('index')

    return render(request, 'pedidos/pedido.html', {
        'breadcrumb': breadcrumb(),
        'carrito': pedido.carrito,
        'pedido': pedido,
    })


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def direccion(request, pedido):
    if not pedido.carrito.productos.exists():
        return redirect('index')

    direccion = pedido.get_or_set_direccion_envio()
    puede_modificar_direccion = request.user.direccion_set.exists()

    return render(request, 'pedidos/direccion.html', {
        'breadcrumb': breadcrumb(direccion=True),
        'carrito': pedido.carrito,
        'direccion': direccion,
        'pedido': pedido,
        'puede_modificar_direccion': puede_modificar_direccion
    })


@login_required(login_url='usuarios:iniciar_sesion')
def seleccionar_direccion(request):
    lista_direcciones = request.user.direcciones

    return render(request, 'pedidos/seleccionar_direccion.html', {
        'lista_direcciones': lista_direcciones,
    })


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def set_direccion(request, pedido, pk):
    direccion = get_object_or_404(Direccion, pk=pk)

    if request.user.id is not direccion.usuario.id:
        return redirect('carritos:carrito')

    pedido.update_direccion_y_costo_envio(direccion)
    return redirect('pedidos:direccion')