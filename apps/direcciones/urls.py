from django.urls import path

from . import views

app_name = 'direcciones'

urlpatterns = [
    path('', views.DireccionesListView.as_view(), name='direcciones'),
    path('crear', views.crear, name='crear'),
]
