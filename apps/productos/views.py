from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Producto
from apps.categorias.models import Categoria


class ProductosEnOfertaListView(ListView):
    template_name = 'productos/ofertas.html'
    context_object_name = 'lista_productos'
    queryset = Producto.objects.filter(oferta=True)
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cantidad_productos'] = context['lista_productos'].count()
        print(context)
        return context


class ProductoDetailView(DetailView):
    template_name = 'productos/producto.html'
    context_object_name = 'producto'

    def get_slug(self):
        return self.kwargs['slug']

    def get_queryset(self):
        return Producto.objects.filter(slug=self.get_slug())


class ProductoBusquedaListView(ListView):
    template_name = 'productos/busqueda.html'
    context_object_name = 'lista_productos'

    def get_queryset(self):
        filtro = Q(titulo__icontains=self.query()) | Q(categoria__nombre__icontains=self.query())
        return Producto.objects.filter(filtro)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['cantidad_productos'] = context['lista_productos'].count()
        return context
