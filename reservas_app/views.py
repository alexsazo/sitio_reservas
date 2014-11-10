# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
def iniciar_sesion(request):
    if request.method == "POST":
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR,
                                         u"Su cuenta se encuentra inactiva, converse con el administrador para solucionar su problema.")
            else:
                messages.add_message(request, messages.ERROR,
                                     u"Error en su contraseña o nombre de usuario. Vuelva a intentarlo.")
    else:
        messages.add_message(request, messages.INFO, u"Ingrese con su usuario")
        formulario = AuthenticationForm()
    return render(request, 'registration/login.html', {'formulario': formulario})


@login_required(login_url="/reservas/login/")
def home(request):
    print request.user.first_name
    return render(request, 'reservas_app/home.html')


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    return render(request, 'reservas_app/profile.html')

def buscarSala(request):
    #if request.method = "POST"
    #salas =
    return render(request, 'reservas_app/profile.html', {'salas' : salas})