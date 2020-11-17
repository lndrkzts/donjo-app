import random
import string

from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone


class CuponManager(models.Manager):
    def get_cupon_valido(self, codigo):
        datetime = timezone.now()
        codigo_obj = self.filter(codigo=codigo).filter(valido_desde__lte=datetime).filter(valido_hasta__gte=datetime).first()

        return codigo_obj if codigo_obj.multiples_usos or not codigo_obj.usado else None


class Cupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)
    valido_desde = models.DateTimeField()
    valido_hasta = models.DateTimeField()
    multiples_usos = models.BooleanField(default=False)
    usado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    objects = CuponManager()

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