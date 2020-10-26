import decimal
import uuid

from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from apps.usuarios.models import User
from apps.carritos.models import Carrito

from .enums import Estado


class Pedido(models.Model):
    id_pedido = models.CharField(max_length=100, null=False, blank=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=Estado.choices, default=Estado.CREADO)
    costo_envio = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_pedido

    def get_total(self):
        return self.carrito.total + self.costo_envio

    def actualizar_total(self):
        self.total = self.get_total()
        self.save()


def set_id_pedido(sender, instance, *args, **kwargs):
    if not instance.id_pedido:
        instance.id_pedido = str(uuid.uuid4())


def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()


pre_save.connect(set_id_pedido, sender=Pedido)
pre_save.connect(set_total, sender=Pedido)
