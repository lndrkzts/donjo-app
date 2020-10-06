from django.urls import path

from . import views

app_name = 'productos'

urlpatterns = [
    path('ofertas', views.ProductosEnOfertaListView.as_view(), name='ofertas'),
    path('<slug:slug_categoria>', views.ProductosPorCategoriaListView.as_view(), name='productos_por_categoria')
]
