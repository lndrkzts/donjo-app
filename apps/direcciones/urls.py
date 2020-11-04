from django.urls import path

from . import views

app_name = 'direcciones'

urlpatterns = [
    path('', views.DireccionListView.as_view(), name='direcciones'),
    path('crear', views.crear, name='crear'),
    path('editar/<int:pk>', views.DireccionUpdateView.as_view(), name='editar'),
    path('eliminar/<int:pk>', views.eliminar_direccion, name='eliminar'),
]
