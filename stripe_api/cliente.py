from . import stripe

def crear_cliente(usuario):
    return stripe.Customer.create(
        description='Se ha creado el cliente del usuario {}'.format(usuario.descripcion),
    )