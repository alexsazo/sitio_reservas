# coding: utf-8
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from model_mommy import mommy


class DocenteTest(TestCase):
    def setUp(self):
        self.docente = mommy.make('Docente')
        self.asignatura = mommy.make('Asignatura', docente=self.docente)
        self.sala = mommy.make('Sala')

        self.right_now = now()
        self.hour = timedelta(hours=1)

    def test_solicitar_reserva(self):
        """
        Prueba el método Docente.solicitar_reserva. Este método recibe
        los datos de la solicitud y devuelve un nuevo objeto de solicitud
        """
        data = {'comienzo': self.right_now,
                'fin': self.right_now+self.hour,
                'asignatura': self.asignatura,
                'sala': self.sala}

        solicitud = self.docente.solicitar_reserva(**data)
        self.assertIsNotNone(solicitud.pk)
        self.assertEqual(solicitud.comienzo, data['comienzo'])
        self.assertEqual(solicitud.fin, data['fin'])
        self.assertEqual(solicitud.asignatura, data['asignatura'])
        self.assertEqual(solicitud.sala, data['sala'])
        self.assertFalse(solicitud.vigente)

    def test_solicitar_reserva_con_fechas_severla(self):
        data = {'comienzo': self.right_now+self.hour,
                'fin': self.right_now,
                'asignatura': self.asignatura,
                'sala': self.sala}

        with self.assertRaises(ValidationError):
            self.docente.solicitar_reserva(**data)
