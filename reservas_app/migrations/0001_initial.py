# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('codigo', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inicio_bloque_matutino', models.DateTimeField()),
                ('q_bloque_matutino', models.IntegerField()),
                ('inicio_bloque_vespertino', models.DateTimeField()),
                ('q_bloque_vespertino', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('run', models.CharField(max_length=11, serialize=False, primary_key=True)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Edificio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comienzo', models.DateTimeField()),
                ('fin', models.DateTimeField()),
                ('serie', models.BooleanField(default=False)),
                ('asignatura', models.ForeignKey(to='reservas_app.Asignatura')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('capacidad', models.IntegerField()),
                ('edificio', models.ForeignKey(to='reservas_app.Edificio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sala_tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_publicacion', models.DateTimeField()),
                ('comienzo', models.DateTimeField()),
                ('horas_cantidad', models.IntegerField()),
                ('docente', models.ForeignKey(to='reservas_app.Docente')),
                ('sala', models.ForeignKey(to='reservas_app.Sala')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sala',
            name='tipo',
            field=models.ForeignKey(to='reservas_app.Sala_tipo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reserva',
            name='sala',
            field=models.ForeignKey(to='reservas_app.Sala'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='docente',
            name='facultad',
            field=models.ForeignKey(to='reservas_app.Facultad'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asignatura',
            name='docente',
            field=models.ForeignKey(to='reservas_app.Docente'),
            preserve_default=True,
        ),
    ]
