from django.contrib import admin
from .models import Categoria


class CategoriaAdmin(admin.ModelAdmin):
    fields = ('nombre', 'activa')
    list_display = ('__str__', 'slug', 'activa', 'fecha_creacion')


admin.site.register(Categoria, CategoriaAdmin)
