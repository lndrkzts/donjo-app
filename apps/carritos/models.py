import uuid

from django.db import models
from django.db.models.signals import pre_save

from apps.usuarios.models import User
from apps.productos.models import Producto


class Carrito(models.Model):
    id_carrito = models.CharField(max_length=100, null=False, blank=False, unique=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="CarritoProducto")
    subtotal = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    RECOMPENSA = 0.05

    def __str__(self):
        return self.id_carrito


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


def set_id_carrito(sender, instance, *args, **kwargs):
    if not instance.id_carrito:
        instance.id_carrito = str(uuid.uuid4())


pre_save.connect(set_id_carrito, sender=Carrito) 
