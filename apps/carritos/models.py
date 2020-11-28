import uuid, decimal

from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from apps.usuarios.models import User
from apps.productos.models import Producto
from apps.pedidos.enums import Estado


class Carrito(models.Model):
    id_carrito = models.CharField(max_length=100, null=False, blank=False, unique=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through="CarritoProducto")
    subtotal = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    COMISION = 5

    def __str__(self):
        return self.id_carrito

    @property
    def pedido(self):
        return self.pedido_set.filter(estado=Estado.CREADO).first()

    def productos_relacionados(self):
        return self.carritoproducto_set.select_related('producto')

    def actualizar_totales(self):
        self.actualizar_subtotal()
        self.actualizar_total()

        if self.pedido:
            self.pedido.actualizar_total()

    def actualizar_subtotal(self):
        self.subtotal = sum([carritoproducto.producto.precio * carritoproducto.cantidad for carritoproducto in self.productos_relacionados()])
        self.save()

    def actualizar_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Carrito.COMISION / 100))
        self.save()

    def verificar_stocks_suficientes(self):
        productos_sin_stock = []

        for carritoproducto in self.productos_relacionados():
            if carritoproducto.cantidad > carritoproducto.producto.stock:
                productos_sin_stock.append(carritoproducto.producto.titulo)
        
        return (len(productos_sin_stock) == 0, productos_sin_stock)


class CarritoProductoManager(models.Manager):
    def crear_o_actualizar_cantidad(self, carrito, producto, cantidad=1):
        objeto, creado = self.get_or_create(carrito=carrito, producto=producto)
    
        if not creado:
            cantidad = objeto.cantidad + cantidad
        objeto.actualizar_cantidad(cantidad)
        
        return objeto


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    objects = CarritoProductoManager()

    def actualizar_cantidad(self, cantidad):
        self.cantidad = cantidad
        self.save()


def set_id_carrito(sender, instance, *args, **kwargs):
    if not instance.id_carrito:
        instance.id_carrito = str(uuid.uuid4())


def post_save_actualizar_totales(sender, instance, *args, **kwargs):
    instance.carrito.actualizar_totales()


def actualizar_totales(sender, instance, action, *args, **kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        instance.actualizar_totales()


pre_save.connect(set_id_carrito, sender=Carrito)
post_save.connect(post_save_actualizar_totales, sender=CarritoProducto)
m2m_changed.connect(actualizar_totales, sender=Carrito.productos.through)
