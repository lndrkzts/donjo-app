import uuid

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from apps.categorias.models import Categoria


class TipoUnidadPeso(models.TextChoices):
    GRAMO = 'Gramo'
    KILO = 'Kilo'
    MILILITRO = 'Mililitro'
    LITRO = 'Litro'


class Producto(models.Model):
    titulo = models.CharField(max_length=50, blank=False, null=False)
    categoria = models.ForeignKey(Categoria, blank=False, null=False, on_delete=models.CASCADE)
    descripcion = models.TextField()
    peso = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    unidad_peso = models.CharField(max_length=50, choices=TipoUnidadPeso.choices, blank=False, null=False)
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    oferta = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='productos/', blank=False, null=False)
    slug = models.SlugField(blank=False, null=False, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


def set_slug(sender, instance, *args, **kwargs):
    if instance.titulo and not instance.slug:
        slug = slugify(instance.titulo)
        while Producto.objects.filter(slug=slug).exists():
            slug = slugify('{}-{}'.format(instance.titulo, str(uuid.uuid4())[:4]))
        instance.slug = slug


pre_save.connect(set_slug, sender=Producto)
