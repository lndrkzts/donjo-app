from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Direccion


class DireccionesListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'direcciones/direcciones.html'
    context_object_name = 'lista_direcciones'

    def get_queryset(self): 
        return Direccion.objects.filter(usuario=self.request.user)
