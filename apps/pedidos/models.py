import decimal
import uuid

from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from apps.carritos.models import Carrito
from apps.cupones.models import Cupon
from apps.direcciones.models import Direccion
from apps.tarjetas.models import Tarjeta
from apps.usuarios.models import User

from .enums import Estado


class Pedido(models.Model):
    id_pedido = models.CharField(max_length=100, null=False, blank=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=Estado.choices, default=Estado.CREADO)
    costo_envio = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    direccion_envio = models.ForeignKey(Direccion, null=True, blank=True, on_delete=models.CASCADE)
    tarjeta = models.ForeignKey(Tarjeta, null=True, blank=True, on_delete=models.CASCADE)
    cupon = models.ForeignKey(Cupon, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_pedido

    @property
    def descripcion(self):
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return 'Compra realizada el día {0} mediante el pedido {1}.'.format(fecha, self.id_pedido)

    def get_descuento(self):
        return self.cupon.descuento if self.cupon else 0

    def get_total(self):
        return self.carrito.total + self.costo_envio - decimal.Decimal(self.get_descuento())

    def actualizar_total(self):
        self.total = self.get_total()
        self.save()

    def get_or_set_direccion_envio(self):
        if self.direccion_envio:
            return self.direccion_envio

        direccion_usuario = self.usuario.direccion_principal

        if direccion_usuario:
            self.update_direccion_y_costo_envio(direccion_usuario)
        return direccion_usuario

    def get_or_set_tarjeta(self):
        if self.tarjeta:
            return self.tarjeta

        tarjeta_usuario = self.usuario.tarjeta_principal

        if tarjeta_usuario:
            self.update_tarjeta(tarjeta_usuario)
        return tarjeta_usuario

    def update_direccion_y_costo_envio(self, direccion_usuario):
        self.direccion_envio = direccion_usuario
        self.costo_envio = direccion_usuario.get_costo_envio()
        self.save()

    def update_tarjeta(self, tarjeta_usuario):
        self.tarjeta = tarjeta_usuario
        self.save()
    
    def cancelar(self):
        self.estado = Estado.CANCELADO
        self.save()
    
    def eliminar(self):
        self.estado = Estado.ELIMINADO
        self.save()
    
    def aplicar_cupon(self, cupon):
        self.cupon = cupon
        self.save()
        self.actualizar_total()
        cupon.marcar_usado()
    
    def setear_como_pago(self):
        self.estado = Estado.PAGO
        self.save()
    
    def mostrar_direccion(self):
        estados_invalidos = [Estado.CREADO, Estado.CANCELADO, Estado.ELIMINADO]
        return self.estado not in estados_invalidos


def set_id_pedido(sender, instance, *args, **kwargs):
    if not instance.id_pedido:
        instance.id_pedido = str(uuid.uuid4())


def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()


pre_save.connect(set_id_pedido, sender=Pedido)
pre_save.connect(set_total, sender=Pedido)
