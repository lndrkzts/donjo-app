from django.urls import path

from .views import iniciar_sesion, cerrar_sesion, registrarse

app_name = 'usuarios'

urlpatterns = [
    path('iniciar_sesion', iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion', cerrar_sesion, name='cerrar_sesion'),
    path('registrarse', registrarse, name='registrarse'),
]
