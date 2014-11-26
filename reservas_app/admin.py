from django.contrib import admin

from reservas_app.models import Reserva, Asignatura, Sala, Solicitud, Docente, Facultad, Configuracion, Periodo, Jefazo

models = [Reserva, Asignatura, Sala, Solicitud, Docente, Facultad, Configuracion, Periodo, Jefazo]

map(lambda x: admin.site.register(x), models)

