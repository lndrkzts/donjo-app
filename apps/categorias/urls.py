from django.urls import path

from . import views

app_name = 'categorias'

urlpatterns = [
    path('<slug:slug>', views.ProductosPorCategoriaListView.as_view(), name='productos_por_categoria'),
]
