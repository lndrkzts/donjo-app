from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from donjo.settings.base import STRIPE_PUBLIC_KEY


@login_required(login_url='usuarios:iniciar_sesion')
def agregar(request):
    if request.method == 'POST':
        if request.POST.get('stripeToken'):
            if not request.user.tiene_id_cliente():
                request.user.crear_id_cliente()

    return render(request, 'tarjetas/agregar.html', {
        'stripe_public_key': STRIPE_PUBLIC_KEY
    })
