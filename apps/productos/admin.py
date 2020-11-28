from django.contrib import admin
from .models import Producto


class ProductAdmin(admin.ModelAdmin):
    fields = ('titulo', 'categoria', 'descripcion', 'peso', 'unidad_peso', 'precio', 'stock', 'oferta', 'imagen')
    list_display = ('__str__', 'slug', 'fecha_creacion')


admin.site.register(Producto, ProductAdmin)
