from django.shortcuts import render
from django.shortcuts import redirect

from apps.productos.models import Producto


def index(request):
    productos = Producto.objects.order_by('?')[0:3]

    return render(request, 'index.html', {
        'lista_productos': productos
    })
