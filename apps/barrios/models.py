from django.db import models


class Barrio(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    costo_envio = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
