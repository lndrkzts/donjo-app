from django.urls import path

from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.PedidosListView.as_view(), name='pedidos'),
    path('pedido', views.pedido, name='pedido'),
]
