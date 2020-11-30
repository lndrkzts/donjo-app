import threading

from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .decorators import get_carrito_and_pedido
from .mails import Mail
from .utils import breadcrumb, eliminar_pedido_session

from apps.cargos.models import Cargo
from apps.direcciones.models import Direccion
from apps.pedidos.models import Pedido
from apps.pedidos.enums import Estado as EstadoPedido
from apps.tarjetas.models import Tarjeta
from apps.usuarios.models import TipoUsuario

from apps.carritos.utils import eliminar_carrito_session


class PedidoDetailView(LoginRequiredMixin, DetailView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'pedidos/detalle.html'
    context_object_name = 'pedido'

    def get_pk(self):
        return self.kwargs['pk']

    def get_queryset(self):
        return Pedido.objects.filter(id=self.get_pk())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carrito'] = context['pedido'].carrito
        context['modo_vista'] = True
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vista_empleado'] = True
        return context


class PedidosAsignadosListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'pedidos/pedidos_asignados.html'
    context_object_name = 'lista_pedidos'
    paginate_by = 10

    def get_queryset(self): 
        return Pedido.objects.filter(estado__in=[EstadoPedido.EN_PREPARACION, EstadoPedido.PREPARADO], empleado_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vista_empleado'] = True
        return context


class PedidosEnviadosListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'pedidos/pedidos_enviados.html'
    context_object_name = 'lista_pedidos'
    paginate_by = 10

    def get_queryset(self): 
        return Pedido.objects.filter(estado=EstadoPedido.ENVIADO, empleado_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vista_empleado'] = True
        return context


class PedidosEntregadosListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'pedidos/pedidos_entregados.html'
    context_object_name = 'lista_pedidos'
    paginate_by = 10

    def get_queryset(self): 
        return Pedido.objects.filter(estado=EstadoPedido.ENTREGADO, empleado_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vista_empleado'] = True
        return context


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
            pedido.setear_pago()
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


@login_required(login_url='usuarios:iniciar_sesion')
def asignar_empleado(request, pk):
    if request.user.tipo_usuario != TipoUsuario.EMPLEADO:
        messages.success(request, 'No tiene permisos para realizar la acción')
        return redirect('index')
    
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.asignar_empleado(request.user)
    pedido.setear_en_preparacion()

    messages.success(request, 'Se te ha asignado el pedido')
    return redirect('pedidos:pendientes')


@login_required(login_url='usuarios:iniciar_sesion')
def preparado(request, pk):
    if request.user.tipo_usuario != TipoUsuario.EMPLEADO:
        messages.error(request, 'No tiene permisos para realizar la acción')
        return redirect('index')
    
    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.empleado != request.user:
        messages.error(request, 'El pedido no está asignado a usted')
        return redirect('index')

    if pedido.estado != EstadoPedido.EN_PREPARACION:
        messages.error(request, 'El pedido no se encuentra en el estado correcto')
        return redirect('index')

    pedido.setear_preparado()

    messages.success(request, 'El pedido se marcó como preparado')
    return redirect('pedidos:asignados')


@login_required(login_url='usuarios:iniciar_sesion')
def enviado(request, pk):
    if request.user.tipo_usuario != TipoUsuario.EMPLEADO:
        messages.error(request, 'No tiene permisos para realizar la acción')
        return redirect('index')
    
    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.empleado != request.user:
        messages.error(request, 'El pedido no está asignado a usted')
        return redirect('index')

    if pedido.estado != EstadoPedido.PREPARADO:
        messages.error(request, 'El pedido no se encuentra en el estado correcto')
        return redirect('index')

    pedido.setear_enviado()

    messages.success(request, 'El pedido se marcó como enviado')
    return redirect('pedidos:enviados')


@login_required(login_url='usuarios:iniciar_sesion')
def entregado(request, pk):
    if request.user.tipo_usuario != TipoUsuario.EMPLEADO:
        messages.error(request, 'No tiene permisos para realizar la acción')
        return redirect('index')
    
    pedido = get_object_or_404(Pedido, pk=pk)

    if pedido.empleado != request.user:
        messages.error(request, 'El pedido no está asignado a usted')
        return redirect('index')

    if pedido.estado != EstadoPedido.ENVIADO:
        messages.error(request, 'El pedido no se encuentra en el estado correcto')
        return redirect('index')

    pedido.setear_entregado()

    messages.success(request, 'El pedido se marcó como entregado')
    return redirect('pedidos:entregados')