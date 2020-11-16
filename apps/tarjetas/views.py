from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView

from donjo.settings.base import STRIPE_PUBLIC_KEY

from .models import Tarjeta


class TarjetaListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'tarjetas/tarjetas.html'
    context_object_name = 'lista_tarjetas'

    def get_queryset(self): 
        return Tarjeta.objects.filter(usuario=self.request.user).order_by('-principal', 'empresa')


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


@login_required(login_url='usuarios:iniciar_sesion')
def principal(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)

    if request.user.id is not tarjeta.usuario.id:
        return redirect('tarjetas:tarjetas')

    if request.user.tiene_tarjeta_principal():
        request.user.tarjeta_principal.update_principal(False)

    tarjeta.update_principal(True)
    messages.success(request, "Se ha modificado la tarjeta principal")
    
    return redirect('tarjetas:tarjetas')