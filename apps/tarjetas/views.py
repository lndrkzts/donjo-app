from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from donjo.settings.base import STRIPE_PUBLIC_KEY

from .models import Tarjeta


@login_required(login_url='usuarios:iniciar_sesion')
def agregar(request):
    if request.method == 'POST':
        stripe_token = request.POST.get('stripeToken')

        if stripe_token:
            if not request.user.tiene_id_cliente():
                request.user.crear_id_cliente()

            tarjeta = Tarjeta.objects.crear_by_stripe_token(request.user, stripe_token)

            if tarjeta:
                messages.success(request, "La tarjeta ha sido agregada exitosamente")

    return render(request, 'tarjetas/agregar.html', {
        'stripe_public_key': STRIPE_PUBLIC_KEY
    })
