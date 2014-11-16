# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
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
                ('inicio_bloque_matutino', models.DateTimeField(verbose_name=b'Inicio de bloque matutino')),
                ('q_bloque_matutino', models.IntegerField(verbose_name=b'Cantidad de horas por bloque')),
                ('inicio_bloque_vespertino', models.DateTimeField(verbose_name=b'Inicio de bloque vespertino')),
                ('q_bloque_vespertino', models.IntegerField(verbose_name=b'Cantidad de horas por bloque')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('rut', models.CharField(max_length=11, serialize=False, primary_key=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('reservas_app.user',),
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
            name='Jefazo',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('reservas_app.user',),
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('semestre', models.IntegerField(choices=[(2, b'SEGUNDO SEMESTRE'), (1, b'PRIMER SEMESTRE')])),
                ('year', models.IntegerField(max_length=4, verbose_name='a\xf1o')),
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
                ('edificio', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Facultad de Ingenier\xc3\xada')])),
                ('tipo', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Normal')])),
                ('capacidad', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('comienzo', models.DateTimeField()),
                ('horas_cantidad', models.IntegerField(verbose_name=b'Cantidad de horas')),
                ('docente', models.ForeignKey(to='reservas_app.Docente')),
                ('sala', models.ForeignKey(to='reservas_app.Sala')),
            ],
            options={
            },
            bases=(models.Model,),
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
            model_name='docente',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='configuracion',
            name='periodo',
            field=models.ForeignKey(to='reservas_app.Periodo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asignatura',
            name='docente',
            field=models.ForeignKey(to='reservas_app.Docente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
