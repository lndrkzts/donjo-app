from django.urls import path

from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.PedidosListView.as_view(), name='pedidos'),
    path('detalle/<int:pk>', views.PedidoDetailView.as_view(), name='detalle'),
    path('pedido', views.pedido, name='pedido'),
    path('direccion', views.direccion, name='direccion'),
    path('seleccionar_direccion', views.seleccionar_direccion, name='seleccionar_direccion'),
    path('set_direccion/<int:pk>', views.set_direccion, name='set_direccion'),
    path('tarjeta', views.tarjeta, name='tarjeta'),
    path('seleccionar_tarjeta', views.seleccionar_tarjeta, name='seleccionar_tarjeta'),
    path('set_tarjeta/<int:pk>', views.set_tarjeta, name='set_tarjeta'),
    path('confirmar', views.confirmar, name='confirmar'),
    path('cancelar', views.cancelar, name="cancelar"),
    path('completar', views.completar, name="completar"),
    path('pendientes', views.PedidosPendientesListView.as_view(), name="pendientes"),
    path('pendientes/asignar_empleado/<int:pk>', views.asignar_empleado, name="asignar_empleado"),
    path('asignados', views.PedidosAsignadosListView.as_view(), name="asignados"),
    path('asignados/preparado/<int:pk>', views.preparado, name="preparado"),
    path('asignados/enviado/<int:pk>', views.enviado, name="enviado"),
    path('enviados', views.PedidosEnviadosListView.as_view(), name="enviados"),
    path('enviados/entregado/<int:pk>', views.entregado, name="entregado"),
    path('entregados', views.PedidosEntregadosListView.as_view(), name="entregados"),
]
