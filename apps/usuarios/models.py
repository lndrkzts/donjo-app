from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.pedidos.enums import Estado


class TipoUsuario(models.TextChoices):
    ADMINISTRADOR = 'ADMINISTRADOR'
    EMPLEADO = 'EMPLEADO'
    CLIENTE = 'CLIENTE'


class User(AbstractUser):
    tipo_usuario = models.CharField(max_length=50, choices=TipoUsuario.choices)

    @property
    def direcciones(self):
        return self.direccion_set.all()

    @property
    def direccion_principal(self):
        return self.direccion_set.filter(principal=True).first()

    def get_nombre_completo(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def pedidos(self):
        return self.pedido_set.exclude(estado=Estado.ELIMINADO).order_by('-id')

    def tiene_direccion_principal(self):
        return self.direccion_principal is not None
