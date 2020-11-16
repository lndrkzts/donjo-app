from django.urls import path

from . import views

app_name = 'tarjetas'

urlpatterns = [
    path('', views.TarjetaListView.as_view(), name='tarjetas'),
    path('agregar', views.agregar, name='agregar'),
    path('principal/<int:pk>', views.principal, name='principal'),
]
