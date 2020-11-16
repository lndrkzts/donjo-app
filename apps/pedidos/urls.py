from django.urls import path

from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.PedidosListView.as_view(), name='pedidos'),
    path('pedido', views.pedido, name='pedido'),
    path('direccion', views.direccion, name='direccion'),
    path('seleccionar_direccion', views.seleccionar_direccion, name='seleccionar_direccion'),
    path('set_direccion/<int:pk>', views.set_direccion, name='set_direccion'),
    path('tarjeta', views.tarjeta, name='tarjeta'),
    path('seleccionar_tarjeta', views.seleccionar_tarjeta, name='seleccionar_tarjeta'),
    path('set_tarjeta/<int:pk>', views.set_tarjeta, name='set_tarjeta'),
    path('confirmar', views.confirmar, name='confirmar'),
    path('cancelar', views.cancelar, name="cancelar"),
]
