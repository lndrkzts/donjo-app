from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from .models import Direccion
from .forms import DireccionForm


class DireccionListView(LoginRequiredMixin, ListView):
    login_url = 'usuarios:inicar_sesion'
    template_name = 'direcciones/direcciones.html'
    context_object_name = 'lista_direcciones'

    def get_queryset(self):
        return Direccion.objects.filter(usuario=self.request.user).order_by('-principal', '-barrio', '-nombre_calle', '-numero_calle')


class DireccionUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    login_url = 'usuarios:iniciar_sesion'
    model = Direccion
    form_class = DireccionForm
    template_name = 'direcciones/editar.html'

    def get_success_url(self):
        return reverse('direcciones:direcciones')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id is not self.get_object().usuario.id:
            messages.success(request, "Direccion editada correctamente")
            return redirect('direcciones:direcciones')
        return super(DireccionUpdateView, self).dispatch(request, *args, **kwargs)


@login_required(login_url='usuarios:iniciar_sesion')
def eliminar(request, pk):
    if request.method == 'POST':
        Direccion.objects.filter(pk=pk).delete()
        return redirect('direcciones:direcciones')

    elif request.method == 'GET':
        direccion = get_object_or_404(Direccion, pk=pk)
        return render(request, 'direcciones/modals/eliminar.html', {
        'direccion': direccion
    })


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

    return render(request, 'direcciones/crear.html', {'form': formulario})


@login_required(login_url='usuarios:iniciar_sesion')
def principal(request, pk):
    direccion = get_object_or_404(Direccion, pk=pk)

    if request.user.id is not direccion.usuario.id:
        return redirect('direcciones:direcciones')

    if request.user.tiene_direccion_principal():
        request.user.direccion_principal.update_principal(False)

    direccion.update_principal(True)
    return redirect('direcciones:direcciones')
