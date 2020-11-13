from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from donjo.settings.base import STRIPE_PUBLIC_KEY


@login_required(login_url='usuarios:iniciar_sesion')
def agregar(request):
    if request.method == 'POST':
        pass

    return render(request, 'tarjetas/agregar.html', {
        'stripe_public_key': STRIPE_PUBLIC_KEY
    })
