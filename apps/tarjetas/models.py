from django.db import models

from apps.usuarios.models import User

from stripe_api.tarjeta import crear_tarjeta


class TarjetaManager(models.Manager):
    def crear_by_stripe_token(self, usuario, stripe_token):
        if usuario.tiene_id_cliente() and stripe_token:
            tarjeta = crear_tarjeta(usuario, stripe_token)

            return self.create(usuario=usuario,
                               token=stripe_token,
                               id_tarjeta=tarjeta.id,
                               ultimos_digitos=tarjeta.last4,
                               empresa=tarjeta.brand,
                               fondos=tarjeta.funding,
                               principal=not usuario.tiene_tarjeta_principal())


class Tarjeta(models.Model):
    id_tarjeta = models.CharField(max_length=50, null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, null=False, blank=False)
    ultimos_digitos = models.CharField(max_length=4, null=False, blank=False)
    empresa = models.CharField(max_length=50, null=False, blank=False)
    fondos = models.CharField(max_length=50, null=False, blank=False)
    principal = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    objects = TarjetaManager()

    def __str__(self):
        return self.id_tarjeta

    def update_principal(self, principal):
        self.principal = principal
        self.save()
