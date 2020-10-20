from django.urls import path

from . import views

app_name = 'carritos'

urlpatterns = [
    path('', views.carrito, name='carrito'),
    path('agregar', views.agregar_producto, name='agregar'),
    path('eliminar/<int:pk>', views.eliminar_producto, name='eliminar'),
]
