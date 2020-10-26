from django.urls import path

from . import views

app_name = 'pedidos'

urlpatterns = [
    path('pedido', views.pedido, name='pedido'),
    path('pedidos', views.PedidosListView.as_view(), name='pedidos'),
]
