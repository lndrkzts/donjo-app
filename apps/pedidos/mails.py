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

    @staticmethod
    def enviar_mail_pedido_en_preparacion(usuario):
        titulo = 'Tú pedido se está preparando'
        template = get_template('pedidos/mails/en_preparacion.html')
        contexto = template.render({'usuario': usuario})
        mail = EmailMultiAlternatives(titulo, 'Mensaje Donjo Service', settings.EMAIL_HOST_USER, [usuario.email])
        mail.attach_alternative(contexto, 'text/html')
        mail.send()
    
    @staticmethod
    def enviar_mail_pedido_preparado(usuario):
        titulo = 'Tú pedido ya está preparado'
        template = get_template('pedidos/mails/preparado.html')
        contexto = template.render({'usuario': usuario})
        mail = EmailMultiAlternatives(titulo, 'Mensaje Donjo Service', settings.EMAIL_HOST_USER, [usuario.email])
        mail.attach_alternative(contexto, 'text/html')
        mail.send()
    
    @staticmethod
    def enviar_mail_pedido_enviado(usuario):
        titulo = 'Tú pedido ya fue enviado'
        template = get_template('pedidos/mails/enviado.html')
        contexto = template.render({'usuario': usuario})
        mail = EmailMultiAlternatives(titulo, 'Mensaje Donjo Service', settings.EMAIL_HOST_USER, [usuario.email])
        mail.attach_alternative(contexto, 'text/html')
        mail.send()
    
    @staticmethod
    def enviar_mail_pedido_entregado(usuario):
        titulo = 'Recibiste tu pedido'
        template = get_template('pedidos/mails/entregado.html')
        contexto = template.render({'usuario': usuario})
        mail = EmailMultiAlternatives(titulo, 'Mensaje Donjo Service', settings.EMAIL_HOST_USER, [usuario.email])
        mail.attach_alternative(contexto, 'text/html')
        mail.send()