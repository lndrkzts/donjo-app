import debug_toolbar

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/productos', include('api.productos.urls')),
    path('', index, name='index'),
    path('categorias/', include('apps.categorias.urls')),
    path('carritos/', include('apps.carritos.urls')),
    path('cupones/', include('apps.cupones.urls')),
    path('direcciones/', include('apps.direcciones.urls')),
    path('pedidos/', include('apps.pedidos.urls')),
    path('productos/', include('apps.productos.urls')),
    path('tarjetas/', include('apps.tarjetas.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
