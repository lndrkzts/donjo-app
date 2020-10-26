from apps.carritos.utils import get_or_create_carrito
from .utils import get_or_create_pedido


def get_carrito_and_pedido(function):
    def internal(request, *args, **kwargs):
        carrito = get_or_create_carrito(request)
        pedido = get_or_create_pedido(carrito, request)
        return function(request, pedido, *args, **kwargs)
    return internal
