from . import stripe


def crear_tarjeta(usuario, token):
    return stripe.Customer.create_source(usuario.id_cliente, source=token)
