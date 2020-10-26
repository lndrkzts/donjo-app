from apps.pedidos.models import Pedido


def get_or_create_pedido(carrito, request):
    pedido = carrito.pedido

    if pedido is None and request.user.is_authenticated:
        pedido = Pedido.objects.create(carrito=carrito, usuario=request.user)

    if pedido:
        request.session['id_pedido'] = pedido.id

    return pedido