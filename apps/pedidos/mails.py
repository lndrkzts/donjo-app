from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse


class Mail:
    @staticmethod
    def enviar_mail_pedido_pago(usuario):
        titulo = 'Se ha realizado el pago del pedido'
        template = get_template('pedidos/mails/pago.html')
        contexto = template.render({'usuario': usuario})
        mail = EmailMultiAlternatives(titulo, 'Mensaje Donjo Service', settings.EMAIL_HOST_USER, [usuario.email])
        mail.attach_alternative(contexto, 'text/html')
        mail.send()