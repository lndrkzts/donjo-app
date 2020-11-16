from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.pedidos.enums import Estado

from stripe_api import cliente


class TipoUsuario(models.TextChoices):
    ADMINISTRADOR = 'ADMINISTRADOR'
    EMPLEADO = 'EMPLEADO'
    CLIENTE = 'CLIENTE'


class User(AbstractUser):
    id_cliente = models.CharField(max_length=100, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=50, choices=TipoUsuario.choices)

    @property
    def direcciones(self):
        return self.direccion_set.all()

    @property
    def tarjetas(self):
        return self.tarjeta_set.all()

    @property
    def direccion_principal(self):
        return self.direccion_set.filter(principal=True).first()

    @property
    def tarjeta_principal(self):
        return self.tarjeta_set.filter(principal=True).first()

    @property
    def descripcion(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.email)

    def get_nombre_completo(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def pedidos(self):
        return self.pedido_set.exclude(estado=Estado.ELIMINADO).order_by('-id')

    def tiene_direccion_principal(self):
        return self.direccion_principal is not None

    def tiene_tarjeta_principal(self):
        return self.tarjeta_principal is not None

    def tiene_id_cliente(self):
        return self.id_cliente is not None
    
    def crear_id_cliente(self):
        cliente_creado = cliente.crear_cliente(self)
        self.id_cliente = cliente_creado.id
        self.save()
