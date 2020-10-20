from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import DeleteView

from apps.productos.models import Producto

from .models import CarritoProducto
from .utils import get_or_create_carrito


def carrito(request):
    carrito = get_or_create_carrito(request)
    return render(request, 'carritos/carrito.html', {
        'carrito': carrito
    })


def agregar_producto(request):
    carrito = get_or_create_carrito(request)
    producto = get_object_or_404(Producto, id=request.POST.get('id_producto'))
    cantidad = int(request.POST.get('inpCantidad', 1))

    CarritoProducto.objects.crear_o_actualizar_cantidad(carrito=carrito, producto=producto, cantidad=cantidad)
    
    return render(request, 'carritos/agregar.html', {
        'producto': producto,
        'cantidad': cantidad
    })


def eliminar_producto(request, pk):
    if request.method == 'POST':
        carrito = get_or_create_carrito(request)
        producto = get_object_or_404(Producto, pk=pk)
        carrito.productos.remove(producto)
        
        return redirect('carritos:carrito')

    elif request.method == 'GET':
        carrito = get_or_create_carrito(request)
        producto = get_object_or_404(Producto, pk=pk)

        return render(request, 'carritos/modals/eliminar.html', {
        'producto': producto
    })
