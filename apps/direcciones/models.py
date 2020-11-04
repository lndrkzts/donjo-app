from django.db import models

from apps.usuarios.models import User
from apps.barrios.models import Barrio


class Direccion(models.Model):
    usuario = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    nombre_calle = models.CharField(max_length=100, null=False, blank=False)
    numero_calle = models.IntegerField(null=False, blank=False)
    barrio = models.ForeignKey(Barrio, null=False, blank=False, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=300)
    principal = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}, {}'.format(self.nombre_calle, self.numero_calle, self.barrio.nombre)

    @property
    def direccion(self):
        return '{} {}, {}'.format(self.nombre_calle, self.numero_calle, self.barrio.nombre)

    def tiene_pedidos_relacionados(self):
        return self.pedido_set.count() >= 1