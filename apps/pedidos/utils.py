from django.urls import reverse

from .models import Pedido
from .enums import Estado


def get_or_create_pedido(carrito, request):
    pedido = carrito.pedido

    if pedido is None and request.user.is_authenticated:
        pedido = Pedido.objects.create(carrito=carrito, usuario=request.user)

    if pedido:
        request.session['id_pedido'] = pedido.id

    return pedido


def eliminar_pedido_session(request):
    request.session['id_pedido'] = None


def breadcrumb(productos=True, direccion=False, tarjeta=False, confirmacion=False):
    return [
        {'titulo': 'Productos', 'activo': productos, 'url': reverse('pedidos:pedido')},
        {'titulo': 'Dirección', 'activo': direccion, 'url': reverse('pedidos:direccion')},
        {'titulo': 'Tarjeta', 'activo': tarjeta, 'url': '#'},
        {'titulo': 'Confirmación', 'activo': confirmacion, 'url': '#'},
    ]
