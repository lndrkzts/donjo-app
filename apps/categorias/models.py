from django.db import models

from apps.productos.models import Producto


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    activa = models.BooleanField(default=True)
    productos = models.ManyToManyField(Producto, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
