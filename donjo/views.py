from django.shortcuts import render
from django.shortcuts import redirect

from apps.productos.models import Producto
from apps.usuarios.models import TipoUsuario


def index(request):
    if request.user.is_anonymous or request.user.tipo_usuario == TipoUsuario.CLIENTE:
        productos = Producto.objects.filter(oferta=True).order_by('precio')[0:6]
        return render(request, 'index.html', { 'lista_productos': productos })

    elif request.user.tipo_usuario == TipoUsuario.EMPLEADO:
        return redirect('pedidos:pendientes') 

    elif request.user.tipo_usuario == TipoUsuario.ADMINISTRADOR:
        return render(request, 'index_administrador.html', {})
