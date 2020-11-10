from .models import Carrito


def get_or_create_carrito(request):
    usuario = request.user if request.user.is_authenticated else None
    id_carrito = request.session.get('id_carrito')
    carrito = Carrito.objects.filter(id_carrito=id_carrito).first()

    if carrito is None:
        carrito = Carrito.objects.create(usuario=usuario)

    if usuario and carrito.usuario is None:
        carrito.usuario = usuario
        carrito.save()

    request.session['id_carrito'] = carrito.id_carrito

    return carrito


def eliminar_carrito_session(request):
    request.session['id_carrito'] = None
