# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracion',
            name='periodo',
            field=models.TextField(default=b'2014 - 2SEM', max_length=20),
            preserve_default=True,
        ),
    ]
