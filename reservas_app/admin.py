from django.contrib import admin

from reservas_app.models import Reserva, Asignatura, Sala, Sala_tipo, Edificio, Solicitud, Docente, Facultad, Configuracion, Periodo

models = [Reserva, Asignatura, Sala, Sala_tipo, Edificio, Solicitud, Docente, Facultad, Configuracion, Periodo]

map(lambda x: admin.site.register(x), models)

