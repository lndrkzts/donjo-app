import random
import string

from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone


class Cupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.FloatField(blank=False, null=False)
    valido_desde = models.DateTimeField()
    valido_hasta = models.DateTimeField()
    multiples_usos = models.BooleanField(default=False)
    usado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo
    
    def marcar_usado(self):
        self.usado = True
        self.save()


def set_codigo(sender, instance, *args, **kwargs):
    if instance.codigo:
        return

    caracteres = string.ascii_uppercase + string.digits
    instance.codigo = ''.join(random.choice(caracteres) for e in range(10))


pre_save.connect(set_codigo, sender=Cupon)