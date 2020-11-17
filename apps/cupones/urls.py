from django.urls import path

from . import views

app_name = 'cupones'

urlpatterns = [
    path('validar', views.validar, name='validar'),
]
