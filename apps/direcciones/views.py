from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from .models import Direccion
from .forms import DireccionForm


class DireccionesListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'direcciones/direcciones.html'
    context_object_name = 'lista_direcciones'

    def get_queryset(self):
        return Direccion.objects.filter(usuario=self.request.user)


@login_required(login_url='usuarios:iniciar_sesion')
def crear(request):
    formulario = DireccionForm(request.POST or None)

    if request.method == 'POST' and formulario.is_valid():
        direccion = formulario.save(commit=False)
        direccion.usuario = request.user
        direccion.principal = not request.user.tiene_direccion_principal()
        direccion.save()
        messages.success(request, 'Dirección creada exitosamente')

        return redirect('direcciones:direcciones')

    return render(request, 'direcciones/crear.html', {'formulario': formulario})
