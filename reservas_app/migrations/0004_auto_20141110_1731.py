# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas_app', '0003_auto_20141110_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('semestre', models.IntegerField(choices=[(2, b'SEGUNDO SEMESTRE'), (1, b'PRIMER SEMESTRE')])),
                ('year', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='periodo',
            field=models.ForeignKey(to='reservas_app.Periodo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_publicacion',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
