__author__ = 'Alex'
from django import forms
from reservas_app.models import *

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = ['vigente']

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
