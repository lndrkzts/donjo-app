from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Producto


class ProductosEnOfertaListView(ListView):
  template_name = 'productos/listado_productos.html'
  context_object_name = 'lista_productos'
  queryset = Producto.objects.all()
  paginate_by = 3
