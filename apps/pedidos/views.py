import threading

from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView

from .decorators import get_carrito_and_pedido
from .mails import Mail
from .utils import breadcrumb, eliminar_pedido_session

from apps.cargos.models import Cargo
from apps.direcciones.models import Direccion
from apps.pedidos.models import Pedido
from apps.pedidos.enums import Estado as EstadoPedido
from apps.tarjetas.models import Tarjeta

from apps.carritos.utils import eliminar_carrito_session


class PedidosListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'pedidos/pedidos.html'
    context_object_name = 'lista_pedidos'
    paginate_by = 10

    def get_queryset(self): 
        return self.request.user.pedidos()


class PedidosPendientesListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'pedidos/pedidos_pendientes.html'
    context_object_name = 'lista_pedidos'
    paginate_by = 10

    def get_queryset(self): 
        return Pedido.objects.filter(estado=EstadoPedido.PAGO)


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def pedido(request, pedido):
    if not pedido.carrito.productos.exists():
        return redirect('index')

    stock_valido = pedido.carrito.verificar_stocks_suficientes()

    if not stock_valido[0]:
        messages.error(request, 'No hay suficiente stock de los productos: {}'.format(', '.join(str(x) for x in stock_valido[1])))
        return redirect('carritos:carrito') 

    return render(request, 'pedidos/pedido.html', {
        'breadcrumb': breadcrumb(),
        'carrito': pedido.carrito,
        'pedido': pedido,
    })


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def direccion(request, pedido):
    if not pedido.carrito.productos.exists():
        return redirect('index')

    direccion = pedido.get_or_set_direccion_envio()
    puede_modificar_direccion = request.user.direccion_set.exists()

    return render(request, 'pedidos/direccion.html', {
        'breadcrumb': breadcrumb(direccion=True),
        'carrito': pedido.carrito,
        'direccion': direccion,
        'pedido': pedido,
        'puede_modificar_direccion': puede_modificar_direccion
    })


@login_required(login_url='usuarios:iniciar_sesion')
def seleccionar_direccion(request):
    lista_direcciones = request.user.direcciones

    return render(request, 'pedidos/seleccionar_direccion.html', {
        'lista_direcciones': lista_direcciones,
    })


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def set_direccion(request, pedido, pk):
    direccion = get_object_or_404(Direccion, pk=pk)

    if request.user.id is not direccion.usuario.id:
        return redirect('carritos:carrito')

    pedido.update_direccion_y_costo_envio(direccion)
    messages.success(request, 'Se ha modificado la dirección')

    return redirect('pedidos:direccion')


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def tarjeta(request, pedido):
    if not pedido.carrito.productos.exists():
        return redirect('index')

    tarjeta = pedido.get_or_set_tarjeta()
    puede_modificar_tarjeta = request.user.tarjeta_set.exists()

    return render(request, 'pedidos/tarjeta.html', {
        'breadcrumb': breadcrumb(direccion=True, tarjeta=True),
        'carrito': pedido.carrito,
        'tarjeta': tarjeta,
        'pedido': pedido,
        'puede_modificar_tarjeta': puede_modificar_tarjeta
    })


@login_required(login_url='usuarios:iniciar_sesion')
def seleccionar_tarjeta(request):
    lista_tarjetas = request.user.tarjetas

    return render(request, 'pedidos/seleccionar_tarjeta.html', {
        'lista_tarjetas': lista_tarjetas,
    })


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def set_tarjeta(request, pedido, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)

    if request.user.id is not tarjeta.usuario.id:
        return redirect('carritos:carrito')

    pedido.update_tarjeta(tarjeta)
    messages.success(request, 'Se ha modificado la tarjeta')

    return redirect('pedidos:tarjeta')


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def confirmar(request, pedido):
    if not pedido.carrito.productos.exists():
        return redirect('carritos:carrito')

    if pedido.direccion_envio is None:
        return redirect('pedidos:direccion')

    if pedido.tarjeta is None:
        return redirect('pedidos:tarjeta') 

    if pedido.total < 400:
        messages.error(request, 'El total de la compra debe ser de al menos de $400 incluidos los descuentos y promociones')

    return render(request, 'pedidos/confirmar.html', {
        'breadcrumb': breadcrumb(direccion=True, tarjeta=True, confirmacion=True),
        'carrito': pedido.carrito,
        'pedido': pedido,
        'direccion': pedido.direccion_envio,
        'tarjeta': pedido.tarjeta,
        'ultimo_paso': True
    })


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def cancelar(request, pedido):
    if request.user.id != pedido.usuario.id:
        return redirect('carritos:carrito')

    pedido.cancelar()
    eliminar_pedido_session(request)
    eliminar_carrito_session(request)
    messages.success(request, 'El pedido ha sido cancelado. Puede volver a crear uno nuevo.')

    return redirect('index')


@login_required(login_url='usuarios:iniciar_sesion')
@get_carrito_and_pedido
def completar(request, pedido):
    if request.user.id != pedido.usuario.id:
        return redirect('carritos:carrito')

    stock_valido = pedido.carrito.verificar_stocks_suficientes()

    if not stock_valido[0]:
        messages.error(request, 'No hay suficiente stock de los productos: {}'.format(', '.join(str(x) for x in stock_valido[1])))
        return redirect('carritos:carrito') 

    cargo = Cargo.objects.crear(pedido)

    if cargo:
        with transaction.atomic():
            pedido.setear_como_pago()
            pedido.restar_stock_productos_comprados()

            thread = threading.Thread(target=Mail.enviar_mail_pedido_pago, args=(request.user,))
            thread.start()       
            
            eliminar_pedido_session(request)
            eliminar_carrito_session(request)

            messages.success(request, 'El pedido ha sido pagado. Un empleado comenzará a prepararlo enseguida. Será notificado al e-mail {}'.format(request.user.email))
            return redirect('index')
    else:
        messages.error(request, 'Ocurrió un error al realizar el pago, por favor intente nuevamente en unos instantes')
        return redirect('carritos:carrito')

