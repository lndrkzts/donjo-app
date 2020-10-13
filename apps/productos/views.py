from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Producto
from apps.categorias.models import Categoria


class ProductosEnOfertaListView(ListView):
    template_name = 'productos/listado_productos.html'
    context_object_name = 'lista_productos'
    queryset = Producto.objects.filter(oferta=True)
    paginate_by = 12


class ProductoDetailView(DetailView):
    template_name = 'productos/producto.html'
    context_object_name = 'producto'

    def get_slug(self):
        return self.kwargs['slug']

    def get_queryset(self):
        return Producto.objects.filter(slug=self.get_slug())