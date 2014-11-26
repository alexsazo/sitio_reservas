from django.conf.urls import patterns, include, url

urlpatterns = patterns('reservas_app.views',
    url(r'^$', 'home', name='home'),
    url(r'^sala/(?P<sala_id>\d+)/$', 'sala_detalle', name='sala_detalle'),
    url(r'^docente/(?P<docente_id>\d+)/$', 'docente_detalle', name='docente_detalle'),
    url(r'^asignatura/(?P<asignatura_id>\w+)/$', 'asignatura_detalle', name='asignatura_detalle'),
    url(r'^/?P<docente_id>\d+/solicitar/$', 'solicitar_sala', name='solicitar_sala'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^login/$', 'iniciar_sesion', name='login'),
    url(r'^logout/$' , 'cerrar_sesion', name='logout'),
    url(r'^search/$', 'buscarSala', name='buscar_sala'),
)
