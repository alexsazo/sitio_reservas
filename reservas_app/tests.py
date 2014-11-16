# coding: utf-8
from django.test import TestCase
from django.utils.timezone import now, timedelta
from model_mommy import mommy


class DocenteTest(TestCase):
    def setUp(self):
        self.docente = mommy.make('Docente')
        self.asignatura = mommy.make('Asignatura', docente=self.docente)
        self.sala = mommy.make('Sala')

    def test_solicitar_reserva(self):
        """
        Prueba el método Docente.solicitar_reserva. Este método recibe
        los datos de la solicitud y devuelve un nuevo objeto de solicitud
        """
        right_now = now()
        hour = timedelta(hours=1)

        data = {'comienzo': right_now,
                'fin': right_now+hour,
                'asignatura': self.asignatura,
                'sala': self.sala}

        solicitud = self.docente.solicitar_reserva(**data)
        self.asserIsNotNone(solicitud.pk)
        self.assertEqual(solicitud.comiendo, data['comienzo'])
        self.assertEqual(solicitud.fin, data['fin'])
        self.assertEqual(solicitud.asignatura, data['asignatura'])
        self.assertEqual(solicitud.sala, data['sala'])
        self.assertFalse(solicitud.vigente)
