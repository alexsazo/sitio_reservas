# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas_app', '0004_auto_20141110_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='year',
            field=models.IntegerField(max_length=4, verbose_name='a\xf1o'),
            preserve_default=True,
        ),
    ]
