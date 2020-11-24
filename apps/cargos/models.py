from django.db import models

from apps.pedidos.models import Pedido
from apps.usuarios.models import User

from stripe_api.cargo import crear_cargo


class CargoManager(models.Manager):
    def crear(self, pedido):
        cargo_stripe = crear_cargo(pedido)

        return self.create(id_cargo=cargo_stripe.id,
                    usuario=pedido.usuario,
                    pedido=pedido,
                    monto=cargo_stripe.amount,
                    metodo_pago=cargo_stripe.payment_method,
                    estado=cargo_stripe.status)


class Cargo(models.Model):
    id_cargo = models.CharField(max_length=50, null=False, blank=False)  # Stripe: Identificador del cargo
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    monto = models.IntegerField()  # Stripe: Monto pagado en centavos
    metodo_pago = models.CharField(max_length=50, blank=False, null=False)  # Stripe: Identificador de la tarjeta
    estado = models.CharField(max_length=50, blank=False, null=False)  # Stripe: Estado del cargo
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    objects = CargoManager()

    def __str__(self):
        return self.id_cargo
