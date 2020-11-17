from django.db import models

from apps.pedidos.models import Pedido
from apps.usuarios.models import User


class Cargo(models.Model):
    id_cargo = models.CharField(max_length=50, null=False, blank=False)  # Stripe: Identificador del cargo
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    monto = models.IntegerField()  # Stripe: Monto pagado en centavos
    metodo_pago = models.CharField(max_length=50, blank=False, null=False)  # Stripe: Identificador de la tarjeta
    estado = models.CharField(max_length=50, blank=False, null=False)  # Stripe: Estado del cargo
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id_cargo
