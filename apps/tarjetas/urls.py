from django.urls import path

from . import views

app_name = 'tarjetas'

urlpatterns = [
    path('agregar', views.agregar, name='agregar'),
]
