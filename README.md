# Donjo APP

Proyecto para la materia Práctica Profesional Supervisada de Sistemas Informáticos de la carrera Técnico Universitario en Sistemas de la UTN.

---

## Módulos
- Barrios
- Cargos
- Categorías
- Cupones
- Direcciones
- Pedidos
- Productos
- Tarjetas
- Usuarios

También posee una api que expone los productos (/api/v1/productos).

## Sobre la aplicación

Cuenta con tres tipos de usuario:
- Administrador: Tiene el poder de dar de la alta, baja y modificacion de todos los registros de todas las entidades
- Empleado: Tiene el poder de asignarse pedidos y realizar el seguimiento del mismo
- Cliente: Puede agregar productos a su carrito, ingresar direcciones de entrega y tarjetas de crédito

El cliente no necesariamente debe estar registrado para poder ingresar, puede hacerlo anónimamente, pero al momento de querer realizar el pedido se le va a pedir que se loguee o se registre. Una vez logueado o registrado, se le va a asignar el carrito que tenía cuando era un usuario anónimo, para no perder la compra.

Cuenta con control de stock, se verifica dos veces. La primera vez al crear el pedido, la segunda al confirmarlo. En el caso de que no haya stock de un producto se le informará al cliente.

El cliente realiza el pago se mediante la plataforma [Stripe](https://stripe.com/). Se pueden usar [tarjetas de prueba](https://stripe.com/docs/testing#cards) que la plataforma brinda. Dependiendo de la región, pueden haber tarjetas que no funcionen.

Se le puede aplicar un cupón de descuento al pedido, debe crearlo el Administrador.

La compra mínima debe ser de $400, contando el descuento del cupón.

Desde el momento que se confirma el pedido, hasta que el mismo fue entregado, ante cada cambio de estado del pedido se le enviará un mail al cliente para tenerlo al tanto.

---

## Requisitos

- [Python 3.8](https://www.python.org/downloads/)

## Instalar dependencias

Dentro del repositorio:
```sh
> pip install requirements.txt
```

## Variables de entorno

Para que funcione correctamente, se deben configurar las siguientes variables de entorno.

Clave secreta de Django:
- DJANGO_SECRET_KEY

Claves de Stripe:
- STRIPE_PUBLIC_KEY
- STRIPE_PRIVATE_KEY

Mail para envio de correos:
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

## Ejecución

Dentro del repositorio:
```sh
> python manage.py migrate --settings=donjo.settings.dev
> python manage.py createsuperuser --settings=donjo.settings.dev
> python manage.py runserver --settings=donjo.settings.dev
```

---

## Endpoint GET /api/v1/productos/

La respuesta tendrá el siguiente formato:
```
[
    {
        "id": 1,
        "categoria": {
            "nombre": "Bebidas"
        },
        "titulo": "Agua",
        "descripcion": "Descripcion del producto",
        "peso": "2.00",
        "unidad_peso": "Litro",
        "precio": "90.50",
        "stock": 10,
        "oferta": false,
        "imagen": "https://...",
        "slug": "agua",
        "fecha_creacion": "2020-10-27T22:59:30.812344Z"
    },
    ...
]
```

**Made with ♥**