from .models import Categoria


def get_categorias_activas(request):
    categorias = Categoria.objects.filter(activa=True)
    return {'categorias': categorias}
