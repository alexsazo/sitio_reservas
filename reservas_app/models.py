#coding:utf-8

from django.db import models

class Reserva(models.Model):
    comienzo = models.DateTimeField()
    fin = models.DateTimeField()
    serie = models.BooleanField(default=False)
    asignatura = models.ForeignKey('Asignatura')
    sala = models.ForeignKey('Sala')
    def __unicode__(self):
        return self.sala.nombre + ' - ' + str(self.comienzo.time()) + ' - ' + self.asignatura.nombre

class Asignatura(models.Model):
    codigo = models.CharField(max_length=15, primary_key=True)
    nombre = models.CharField(max_length=50)
    docente = models.ForeignKey('Docente')
    def __unicode__(self):
        return self.codigo + ' - ' + self.nombre

class Sala(models.Model):
    nombre = models.CharField(max_length=50)
    edificio = models.ForeignKey('Edificio')
    tipo = models.ForeignKey('Sala_tipo')
    capacidad = models.IntegerField()
    def __unicode__(self):
        return self.nombre

class Sala_tipo(models.Model):
    nombre = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre

class Edificio(models.Model):
    nombre = models.CharField(max_length=10)
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

class Docente(models.Model):
    run = models.CharField(max_length=11, primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    facultad = models.ForeignKey('Facultad')
    def __unicode__(self):
        return self.run + ' - ' + self.nombres + ' ' + self.apellidos

class Facultad(models.Model):
    nombre = models.CharField(max_length=50)
    def __unicode__(self):
        return self.nombre

class Configuracion(models.Model):
    inicio_bloque_matutino = models.DateTimeField(verbose_name="Inicio de bloque matutino")
    q_bloque_matutino = models.IntegerField(verbose_name="Cantidad de horas por bloque")
    inicio_bloque_vespertino = models.DateTimeField(verbose_name="Inicio de bloque vespertino")
    q_bloque_vespertino = models.IntegerField(verbose_name="Cantidad de horas por bloque")
    periodo = models.ForeignKey('Periodo')
    def __unicode__(self):
        return str(self.pk) + " - " + str(self.periodo)

class Periodo(models.Model):
    semestre = models.IntegerField(choices={(1,'PRIMER SEMESTRE'), (2,'SEGUNDO SEMESTRE')})
    year =  models.IntegerField(max_length=4, verbose_name=u"año")
    def __unicode__(self):
        return str(self.year)  + " - " + "SEM:"+ str(self.semestre)