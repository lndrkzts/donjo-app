from . import stripe

def crear_cargo(pedido):
    if pedido.tarjeta and pedido.usuario and pedido.usuario.id_cliente:
        return stripe.Charge.create(
            amount=int(pedido.total) * 100,
            currency='ARS',
            description=pedido.descripcion,
            customer=pedido.usuario.id_cliente,
            source=pedido.tarjeta.id_tarjeta,
            metadata={'id_pedido': pedido.id},
        )