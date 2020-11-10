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


def eliminar_pedido(pedido):
    pedido.estado = Estado.ELIMINADO
    pedido.save()


def breadcrumb(productos=True, direccion=False, metodo_pago=False, confirmacion=False):
    return [
        {'titulo': 'Productos', 'activo': productos, 'url': reverse('pedidos:pedido')},
        {'titulo': 'Dirección', 'activo': direccion, 'url': reverse('pedidos:direccion')},
        {'titulo': 'Pago', 'activo': metodo_pago, 'url': '#'},
        {'titulo': 'Confirmación', 'activo': confirmacion, 'url': '#'},
    ]
