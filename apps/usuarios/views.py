from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import FormularioRegistro


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        user = authenticate(username=usuario, password=contrasena)

        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else:
            messages.error(
                request, 'El usuario o contraseña ingresado es incorrecto')

    return render(request, 'usuarios/iniciar_sesion.html', {})


def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Esperamos que vuelva pronto!')
    return redirect('usuarios:iniciar_sesion')


def registrarse(request):
    if request.user.is_authenticated:
        return redirect('index')

    formulario = FormularioRegistro(request.POST or None)

    if request.method == "POST" and formulario.is_valid():
        user = formulario.save()

        if user:
            login(request, user)
            messages.success(
                request, 'Usuario creado exitosamente. Bienvenido {}'.format(user.username))
            return redirect('index')

    return render(request, 'usuarios/registrarse.html', {
        'formulario': formulario
    })
