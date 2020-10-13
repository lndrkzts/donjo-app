from django.shortcuts import render
from django.shortcuts import redirect

from apps.productos.models import Producto


def index(request):
    productos = Producto.objects.filter(oferta=True).order_by('precio')[0:6]

    return render(request, 'index.html', {
        'lista_productos': productos
    })
