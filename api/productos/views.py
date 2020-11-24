from rest_framework.response import Response
from rest_framework.views import APIView

from apps.productos.models import Producto
from .serializer import ProductoSerializer


class ListaProducto(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        productos_json = ProductoSerializer(productos, many=True)
        return Response(productos_json.data)
