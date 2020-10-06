from django.db import models

from django.db.models.signals import pre_save
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(blank=False, null=False, unique=True) 
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


def set_slug(sender, instance, *args, **kwargs):
    if instance.nombre and not instance.slug:
        slug = slugify(instance.nombre)
        while Categoria.objects.filter(slug=slug).exists():
            slug = slugify('{}-{}'.format(instance.nombre, str(uuid.uuid4())[:4]))
        instance.slug = slug


pre_save.connect(set_slug, sender=Categoria)