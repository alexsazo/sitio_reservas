# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from reservas_app.models import Sala, Reserva

from django.utils.timezone import now, timedelta, datetime

VERBOSE_DAYS = {
    'LUNES':0,
    'MARTES':1,
    'MIERCOLES':2,
    'JUEVES':3,
    'VIERNES':4,
    'SABADO':5,
    'DOMINGO':6,
}

INICIO_SEMANA = VERBOSE_DAYS['LUNES']
TERMINO_SEMANA = VERBOSE_DAYS['VIERNES']

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

@login_required()
def sala(request, sala_id):
    sala = get_object_or_404(Sala, pk=sala_id)
    list_reservas = Reserva.objects.filter(sala=sala_id)

    return render(request, 'reservas_app/sala_detail.html', {'sala': sala})

@login_required()
def buscarSala(request):
    if request.method == "POST":
        salas = Sala.objects.filter(nombre__icontains=request.POST['busqueda'])
        return render(request, 'reservas_app/find.html', {'salas' : salas})
    return render(request, 'reservas_app/find.html',{'salas': None})

def get_allReservas_from_week(fecha=now(), sala_def=None, docente_def=None):
    lunes = fecha - timedelta(days=(fecha.weekday()-INICIO_SEMANA))
    viernes = fecha + timedelta(days=(TERMINO_SEMANA - fecha.weekday()))

    if sala_def != None and docente_def != None:
        return None
    if sala_def != None:
        return Reserva.objects.filter(sala=sala_def, comienzo__gte=lunes, comienzo__lte=viernes)
    if docente_def != None:
        return  Reserva.objects.filter(docente=docente_def, comienzo__gte=lunes, comienzo__lte=viernes)
