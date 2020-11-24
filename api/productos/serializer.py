from rest_framework import serializers

from apps.categorias.models import Categoria
from apps.productos.models import Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('nombre',)

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
