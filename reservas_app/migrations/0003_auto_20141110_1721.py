# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas_app', '0002_configuracion_periodo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracion',
            name='periodo',
            field=models.CharField(default=b'2014 - 2SEM', max_length=20),
            preserve_default=True,
        ),
    ]
