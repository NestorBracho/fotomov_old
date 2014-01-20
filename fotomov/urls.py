from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fotomov.views.home', name='home'),
    # url(r'^fotomov/', include('fotomov.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'staff.views.ingresar'),
    url(r'^nueva_marca/$', 'marca.views.nueva_marca'),
    url(r'^nuevo_macrocliente/$', 'clientes.views.nuevo_macrocliente'),
    url(r'^listar_macroclientes/(?P<creado>\d+)/$', 'clientes.views.listar_marcroclientes'),
    url(r'^listar_marcas/(?P<creado>\d+)/$', 'marca.views.listar_marcas'),
    url(r'^ver_marca/(?P<id_marca>\d+)/(?P<creado>\d+)/$', 'marca.views.ver_marca'),
    url(r'^nueva_submarca/(?P<id_marca>\d+)/$', 'marca.views.nueva_submarca'),
    url(r'^editar_marca/(?P<id_marca>\d+)/$', 'marca.views.editar_marca'),
    url(r'^editar_submarca/(?P<id_submarca>\d+)/$', 'marca.views.editar_submarca'),
    url(r'^registro/$', 'staff.views.contacto'),
    url(r'^prueba/$', 'staff.views.notificacion'),
    url(r'^nuevo_usuario/$', 'staff.views.nuevo_usuario'),
    url(r'^listar_usuario/$', 'staff.views.lista_usuario'),
)
