from django import template

register = template.Library()


@register.filter
def agregar_formato_cantidad(cantidad):
    return '{} {} {} al carrito'.format(cantidad, 'productos' if cantidad > 1 else 'producto', 'agregados' if cantidad > 1 else 'agregado')


@register.filter
def multiplicar(precio, cantidad):
    return precio * cantidad
