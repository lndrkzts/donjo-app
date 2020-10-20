from django.db import models

from apps.usuarios.models import Usuario
from apps.carritos.models import Carrito


class Estado(models.TextChoices):
    ELIMINADO = 'Eliminado'
    CREADO = 'Creado'
    PAGO = 'Pago'
    EN_PREPARACION = 'En Preparacion'
    PREPARADO = 'Preparado'
    ENVIADO = 'Enviado'
    ENTREGADO = 'Entregado'


class Pedido(models.Model):
    id_pedido = models.CharField(max_length=100, null=False, blank=False, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=Estado)
    costo_envio = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_pedido
