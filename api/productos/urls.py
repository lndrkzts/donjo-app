from django.urls import path

from . import views

app_name = 'api_productos'

urlpatterns = [
    path('', views.ListaProducto.as_view(), name='productos'),
]
