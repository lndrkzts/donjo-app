from django.urls import path

from .views import ProductosEnOfertaListView

app_name = 'productos'

urlpatterns = [
    path('ofertas', ProductosEnOfertaListView.as_view(), name='ofertas'),
]
