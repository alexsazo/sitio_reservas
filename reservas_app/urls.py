from django.conf.urls import patterns, include, url

urlpatterns = patterns('reservas_app.views',
    url(r'^home/$', 'home', name='home'),
    url(r'^home/$', 'buscarSala', name='buscar_sala'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^login/$', 'iniciar_sesion', name='login'),
    url(r'^logout/$' , 'cerrar_sesion', name='logout'),
)
