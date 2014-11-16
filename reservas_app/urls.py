from django.conf.urls import patterns, include, url

urlpatterns = patterns('reservas_app.views',
    url(r'^$', 'home', name='home'),
    url(r'^(?P<sala_id>\d+)/sala/$', 'sala', name='sala'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^login/$', 'iniciar_sesion', name='login'),
    url(r'^logout/$' , 'cerrar_sesion', name='logout'),
    url(r'^search/$', 'buscarSala', name='buscar_sala'),
)
