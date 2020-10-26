from django.db import models


class Estado(models.TextChoices):
    ELIMINADO = 'Eliminado'
    CREADO = 'Creado'
    PAGO = 'Pago'
    EN_PREPARACION = 'En Preparacion'
    PREPARADO = 'Preparado'
    ENVIADO = 'Enviado'
    ENTREGADO = 'Entregado'