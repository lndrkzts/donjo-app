from django.views.generic.list import ListView

from apps.productos.models import Producto
from apps.categorias.models import Categoria


class ProductosPorCategoriaListView(ListView):
    template_name = 'categorias/listado_productos_por_categoria.html'
    context_object_name = 'lista_productos'
    paginate_by = 12

    def get_slug(self):
        return self.kwargs['slug']

    def get_nombre_categoria(self):
        return Categoria.objects.filter(slug=self.get_slug()).first().nombre

    def get_queryset(self):
        return Producto.objects.filter(categoria__slug=self.get_slug())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre_categoria'] = self.get_nombre_categoria()
        context['cantidad_productos'] = context['lista_productos'].count()
        return context
