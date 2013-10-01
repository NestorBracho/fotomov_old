from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'manager.views.hacer_pedido'),
    url(r'^pedidos$', 'manager.views.pedidos'),
    url(r'^datos$', 'manager.views.datos_client'),
    url(r'^todos_pedidos$', 'manager.views.pedidos_admin'),
    url(r'^mod_pedidos/$', 'manager.views.modif_pedidos'),
)
