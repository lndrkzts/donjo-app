from django.db import models
from django.contrib.auth.models import AbstractUser


class TipoUsuario(models.TextChoices):
    ADMINISTRADOR = 'ADMINISTRADOR'
    EMPLEADO = 'EMPLEADO'
    CLIENTE = 'CLIENTE'


class User(AbstractUser):
    tipo_usuario = models.CharField(max_length=50, choices=TipoUsuario.choices)

    def get_nombre_completo(self):
        return '{} {}'.format(self.first_name, self.last_name)
