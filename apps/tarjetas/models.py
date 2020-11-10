from django.db import models

from apps.usuarios.models import User

class Tarjeta(models.Model):
    id_tarjeta = models.CharField(max_length=50, null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, null=False, blank=False)
    ultimos_digitos = models.CharField(max_length=4, null=False, blank=False)
    empresa = models.CharField(max_length=50, null=False, blank=False)
    principal = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_id

    def update_principal(self, principal):
        self.principal = principal
        self.save()