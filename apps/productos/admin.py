from django.contrib import admin
from .models import Producto


class ProductAdmin(admin.ModelAdmin):
    fields = ('titulo', 'descripcion', 'peso', 'unidad_peso', 'precio', 'oferta', 'imagen')
    list_display = ('__str__', 'slug', 'fecha_creacion')


admin.site.register(Producto, ProductAdmin)
