# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from reservas_app.forms import ReservaForm
from reservas_app.models import Sala, Reserva, Configuracion, Periodo, Docente, Asignatura
from django.views.generic import ListView, CreateView
from reservas_app.mixins import *

from django.utils.timezone import now, timedelta, datetime, make_aware, localtime, get_default_timezone

UTC_ADJUST = timedelta(hours=3)
DAYS_TO_ID = {
    'LUNES':0,
    'MARTES':1,
    'MIERCOLES':2,
    'JUEVES':3,
    'VIERNES':4,
    'SABADO':5,
    'DOMINGO':6,
}
DAYS_TO_STRING = {
    0:'LUNES',
    1:'MARTES',
    2:'MIERCOLES',
    3:'JUEVES',
    4:'VIERNES',
    5:'SABADO',
    6:'DOMINGO',
}

INICIO_SEMANA = DAYS_TO_ID['LUNES']
TERMINO_SEMANA = DAYS_TO_ID['VIERNES']


class DocenteListView(SearchableListMixin, ListView):
    model = Docente
    template_name = 'reservas_app/lista_docentes.html'

class SalaListView(ListView):
    model = Sala
    template_name = 'reservas_app/lista_salas.html'

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


def validar_usuario_docente(u):
    try:
        var = u.docente
        return True
    except:
        return False

@login_required(login_url="/reservas/login/")
@user_passes_test(lambda u: validar_usuario_docente(u))
def solicitar_sala(request):
    docente = request.user.docente
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            docente.solicitar_reserva(**form.cleaned_data)
    return render(request, 'reservas_app/solicitar_reserva.html' )


def validar_usuario_jefazo(u):
     try:
        var = u.jefazo
        return True
     except:
        return False

@login_required()
@user_passes_test(lambda u: validar_usuario_jefazo(u))
def listar_docentes(request):
    docentes_list = Docente.objects.all()
    render(request, 'reservas_app/listar_docentes.html', {'docentes': docentes_list})

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
def sala_detalle(request, sala_id):
    sala = get_object_or_404(Sala, pk=sala_id)
    list = get_all_reservas_from_week(sala_def=sala_id)
    list_reservas = reservas_to_format(list)
    return render(request, 'reservas_app/sala_detail.html', {'sala': sala, 'reservas_list': list_reservas})

@login_required()
def docente_detalle(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    if Asignatura.objects.filter(docente=docente):
        list = get_all_reservas_from_week(docente_def=docente.pk)
        list_reservas = reservas_to_format(list)
    else:
        list_reservas = None
    return render(request, 'reservas_app/docente_detalle.html', {'docente': docente, 'reservas_list': list_reservas})

@login_required()
def asignatura_detalle(request, asignatura_id):
    asignatura = get_object_or_404(Asignatura, pk=asignatura_id)
    list = []
    list = get_all_reservas_from_week(asignatura_def=asignatura_id)
    list_reservas = reservas_to_format(list)
    return render(request, 'reservas_app/asignatura_detalle.html', {'asignatura': asignatura, 'reservas_list': list_reservas})

@login_required()
def buscarSala(request):
    if request.method == "POST":
        salas = Sala.objects.filter(nombre__icontains=request.POST['busqueda'])
        return render(request, 'reservas_app/find.html', {'salas' : salas})
    return render(request, 'reservas_app/find.html',{'salas': None})

def reservas_to_format(reservas_list):
    """Esta funcion devuelve el horario completo semanal de un profesor o reserva."""
    reservas_list = sorted(reservas_list, key=lambda x: x.comienzo)
    p = get_periodo_actual()
    c = Configuracion.objects.get(periodo=Periodo.objects.get(**p))
    blocklist = c.get_blocklist()
    grid = map(lambda x: [blocklist[x].get_string(),0,0,0,0,0],range(len(blocklist)))

    for day in ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']:
        for i, block  in enumerate(blocklist):
            for reserva in reservas_list:
                aware_inicio = localtime(make_aware(datetime.combine(reserva.comienzo, block.inicio), get_default_timezone()))
                aware_fin = localtime(make_aware(datetime.combine(reserva.comienzo, block.fin), get_default_timezone()))
                local_r_comienzo = localtime(reserva.comienzo)
                local_r_fin = localtime(reserva.fin)
                print aware_inicio, aware_fin
                if DAYS_TO_ID[day] == reserva.get_weekday():
                    for hora in range(reserva.get_horas_academicas()):
                        u"""Esto rellena inmediatamente las horas académicas siguientes cuando esta reserva ocupa más de 1 hora académica."""
                        print "llegue a hora...", hora
                        diff = timedelta(seconds=(c.duracion_hora_academica*60*hora))
                        block_inicio = aware_inicio + diff
                        block_fin = aware_fin + diff
                        reserva_inicio = reserva.comienzo + diff
                        reserva_inicio_to_compare = reserva_inicio + timedelta(seconds=c.duracion_hora_academica*60)
                        if reserva_inicio >= block_inicio and reserva_inicio_to_compare <= block_fin:
                            if i+hora <= len(grid):
                                print "guarde"
                                grid[i+hora][DAYS_TO_ID[day]+1] = reserva
                            else:
                                pass
    print "mi grid: ", grid
    return grid

def  get_all_reservas_from_week(fecha=now(), sala_def=None, docente_def=None, asignatura_def=None):
    fecha_local = localtime(fecha)
    fecha_superior = datetime(fecha_local.year,fecha_local.month, fecha_local.day-1, 0,0)
    fecha_inferior = datetime(fecha_local.year,fecha_local.month, fecha_local.day, 0,0)

    lunes = fecha_local - timedelta(days=(fecha_inferior.weekday()-INICIO_SEMANA))
    viernes = fecha_local + timedelta(days=(TERMINO_SEMANA - fecha_superior.weekday()))

    print 'viernes : %s' %viernes
    print 'lunes : %s' %lunes

    if sala_def:
        return Reserva.objects.filter(sala=sala_def, comienzo__range=(lunes, viernes))
    elif docente_def:
        return  Reserva.objects.filter(asignatura=get_object_or_404(Asignatura, docente=docente_def), comienzo__range=(lunes, viernes))
    elif asignatura_def:
        return  Reserva.objects.filter(asignatura=asignatura_def, comienzo__range=(lunes, viernes))
def get_periodo_actual():
    if datetime.now().month > 6:
        semestre_actual = 2
    else:
        semestre_actual = 1

    return {'semestre':semestre_actual, 'year':datetime.now().year}



