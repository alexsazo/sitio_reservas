# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from model_utils.managers import InheritanceManager
from django.utils.timezone import now, timedelta, datetime

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

class UserInheritanceManager(InheritanceManager, UserManager):
    pass


class User(AbstractUser):
    objects = UserInheritanceManager()


class Jefazo(User):
    objects = UserInheritanceManager()


class Docente(User):
    rut = models.CharField(max_length=11, primary_key=True)
    facultad = models.ForeignKey('Facultad')

    def solicitar_reserva(self, **kwargs):
        if kwargs['comienzo'] < kwargs['fin']:
            return Reserva.objects.create(**kwargs)
        else:
            raise ValidationError(_(u'Las fechas no son válidas.'), code='invalid')
    # def __unicode__(self):
    #     return self.run + ' - ' + self.nombres + ' ' + self.apellidos


class Reserva(models.Model):
    comienzo = models.DateTimeField()
    fin = models.DateTimeField()
    serie = models.BooleanField(default=False)
    asignatura = models.ForeignKey('Asignatura', null=True, blank=True)
    sala = models.ForeignKey('Sala')
    vigente = models.BooleanField(default=False)

    #@property
    def __unicode__(self):
        return self.sala.nombre + ' - ' + DAYS_TO_STRING[self.comienzo.weekday()] + ' - ' + self.asignatura.nombre + ' - ' + self.asignatura.docente.get_full_name()

    def get_horas_academicas(self):
        return (self.fin - self.comienzo).seconds/60/45

    def get_weekday(self):
        return self.comienzo.weekday()

class Asignatura(models.Model):
    codigo = models.CharField(max_length=15, primary_key=True, unique=True)
    nombre = models.CharField(max_length=50)
    docente = models.ForeignKey('Docente')

    def __unicode__(self):
        return self.codigo + ' - ' + self.nombre


class Sala(models.Model):
    NORMAL = 1

    TIPO_CHOICES = ((NORMAL, 'Normal'),)

    AULAS_A = 1
    AULAS_B = 2
    AULAS_C = 3

    EDIFICIO_CHOICES = ((AULAS_A, 'Aulas B'),
                        (AULAS_B, 'Aulas A'),
                        (AULAS_C, 'Aulas C'),
    )

    nombre = models.CharField(max_length=50, unique=True)
    edificio = models.PositiveSmallIntegerField(choices=EDIFICIO_CHOICES, default=AULAS_A)
    tipo = models.PositiveSmallIntegerField(choices=TIPO_CHOICES, default=NORMAL)
    capacidad = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.nombre


class Solicitud(models.Model):
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    comienzo = models.DateTimeField()
    horas_cantidad = models.IntegerField(verbose_name="Cantidad de horas")
    sala = models.ForeignKey('Sala')
    docente = models.ForeignKey('Docente')

    def __unicode__(self):
        return str(self.sala) + ' - ' + str(self.comienzo) + ' - ' + str(self.docente)


class Facultad(models.Model):
    nombre = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nombre


class Configuracion(models.Model):
    duracion_hora_academica = models.IntegerField(max_length=2, default=45, verbose_name=u"Duración hora académica (minutos)")
    inicio_bloque_matutino = models.TimeField(verbose_name="Inicio de bloque matutino")
    q_bloque_matutino = models.IntegerField(verbose_name="Cantidad de horas por bloque")
    inicio_bloque_vespertino = models.TimeField(verbose_name="Inicio de bloque vespertino")
    q_bloque_vespertino = models.IntegerField(verbose_name="Cantidad de horas por bloque")
    periodo = models.ForeignKey('Periodo', unique=True)

    def __unicode__(self):
        return str(self.duracion_hora_academica) + "min" + " - " + str(self.periodo)

    def get_blocklist(self):
        class Block:
            def __init__(self, inicio, fin):
                self.inicio = inicio
                self.fin = fin

            def get_inicio2String(self):
                return str(self.inicio).split('.')[0]

            def get_fin2String(self):
                return str(self.fin).split('.')[0]

            def get_tuple(self):
                return (self.inicio, self.fin)

            def get_tuple_toString(self):
                return (str(self.inicio).split('.')[0], str(self.fin).split('.')[0])

            def get_string(self):
                return str(self.inicio).split('.')[0] + ' - ' + str(self.fin).split('.')[0]

        def addSecs(tm, secs):
            fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
            fulldate = fulldate + timedelta(seconds=secs)
            return fulldate.time()

        block_list = []
        duracion = self.duracion_hora_academica * 60
        recreo = 5 * 60
        var = self.inicio_bloque_matutino
        for n in range(self.q_bloque_matutino):
            block_list.append(Block(var, addSecs(var, duracion)))
            var = addSecs(var, duracion)
            var = addSecs(var, recreo)
        var = self.inicio_bloque_vespertino
        for n in range(self.q_bloque_vespertino):
            block_list.append(Block(var, addSecs(var, duracion)))
            var = addSecs(var, duracion)
            var = addSecs(var, recreo)
        return block_list


class Periodo(models.Model):
    semestre = models.IntegerField(choices={(1, 'PRIMER SEMESTRE'), (2, 'SEGUNDO SEMESTRE')})
    year = models.IntegerField(max_length=4, verbose_name=u"año")

    def __unicode__(self):
        return str(self.year) + " - " + "SEM:" + str(self.semestre)
