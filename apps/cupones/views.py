from django.shortcuts import render
from django.http import JsonResponse

from apps.pedidos.decorators import get_carrito_and_pedido

from .models import Cupon


@get_carrito_and_pedido
def validar(request, pedido):
    codigo = request.GET.get('codigo')
    cupon = Cupon.objects.get_cupon_valido(codigo)

    if cupon is None:
        return JsonResponse({
            'valido': False
        }, status=404)

    pedido.aplicar_cupon(cupon)

    return JsonResponse({
        'valido': True,
        'codigo': cupon.codigo,
        'descuento': cupon.descuento,
        'total': pedido.total,
    }, status=200)
