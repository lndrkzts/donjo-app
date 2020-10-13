from django.urls import path

from . import views

app_name = 'productos'

urlpatterns = [
    path('ofertas', views.ProductosEnOfertaListView.as_view(), name='ofertas'),
    path('<slug:slug>', views.ProductoDetailView.as_view(), name='producto'),
]
