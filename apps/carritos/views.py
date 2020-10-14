from django.shortcuts import render

from .utils import get_or_create_carrito


def carrito(request):
    carrito = get_or_create_carrito(request)
    return render(request, 'carritos/carrito.html', {
        'carrito': carrito
    })
