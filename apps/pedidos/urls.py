from django.urls import path

from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.PedidosListView.as_view(), name='pedidos'),
    path('pedido', views.pedido, name='pedido'),
    path('direccion', views.direccion, name='direccion'),
    path('seleccionar_direccion', views.seleccionar_direccion, name='seleccionar_direccion'),
    path('set_direccion/<int:pk>', views.set_direccion, name='set_direccion'),
]
