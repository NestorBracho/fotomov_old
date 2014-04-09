from django.conf.urls import patterns, include, url
from fotomov import settings
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
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    url(r'^escritorio/$', 'staff.views.escritorio'),
    url(r'^nueva_marca/$', 'marca.views.nueva_marca'),
    url(r'^nuevo_evento/$', 'evento.views.nuevo_evento'),
    url(r'^nuevo_macrocliente/$', 'clientes.views.nuevo_macrocliente'),
    url(r'^listar_contactos_macrocliente/(?P<id_macrocliente>\d+)/(?P<creado>\d+)/$', 'clientes.views.listar_contactos_macrocliente'),
    url(r'^eliminar_contacto_macrocliente/(?P<id_contacto>\d+)/$', 'clientes.views.eliminar_contacto_macrocliente'),
    url(r'^listar_macroclientes/(?P<creado>\d+)/$', 'clientes.views.listar_macroclientes'),
    url(r'^nuevo_contacto_macrocliente/(?P<id_macrocliente>\d+)/$', 'clientes.views.nuevo_contacto_macrocliente'),
    url(r'^editar_contacto_macrocliente/(?P<id_contacto>\d+)/$', 'clientes.views.editar_contacto_macrocliente'),
    url(r'^ver_contacto/(?P<id_contacto>\d+)/$', 'clientes.views.ver_contacto_macrocliente'),
    url(r'^listar_marcas/(?P<creado>\d+)/$', 'marca.views.listar_marcas'),
    url(r'^ver_marca/(?P<id_marca>\d+)/(?P<creado>\d+)/$', 'marca.views.ver_marca'),
    url(r'^nueva_submarca/(?P<id_marca>\d+)/$', 'marca.views.nueva_submarca'),
    url(r'^editar_marca/(?P<id_marca>\d+)/$', 'marca.views.editar_marca'),
    url(r'^editar_submarca/(?P<id_submarca>\d+)/$', 'marca.views.editar_submarca'),
    url(r'^registro/$', 'staff.views.contacto'),
    url(r'^prueba/$', 'staff.views.notificacion'),
    url(r'^nuevo_usuario/$', 'staff.views.nuevo_usuario'),
    url(r'^listar_usuario/(?P<creado>\d+)/$', 'staff.views.lista_usuario'),
    url(r'^editar_macrocliente/(?P<id_macrocliente>\d+)/$', 'clientes.views.editar_macrocliente'),
    url(r'^eliminar_macrocliente/(?P<id_macrocliente>\d+)/$', 'clientes.views.eliminar_macrocliente'),
    url(r'^ver_macrocliente/(?P<id_macrocliente>\d+)/$', 'clientes.views.ver_macrocliente'),
    url(r'^eliminar_usuario/(?P<id_usuario>\d+)/$', 'staff.views.eliminar_usuario'),
    url(r'^eliminar_marca/(?P<id_marca>\d+)/$', 'marca.views.eliminar_marca'),
    url(r'^modificar_usuario/(?P<id_usuario>\d+)/$', 'staff.views.modificar_usuario'),
    url(r'^ver_usuario/(?P<id_usuario>\d+)/$', 'staff.views.ver_usuario'),
    url(r'^macrocliente_ajax/$', 'clientes.views.nuevo_macrocliente_ajax'),
    url(r'^configurar_staff/(?P<creado>\d+)/$', 'staff.views.configurar_staff'),
    url(r'^eliminar_privilegio/(?P<id_borrar>\d+)/$', 'staff.views.eliminar_staff'),
    url(r'^modificar_staff/(?P<id_modificar>\d+)/$', 'staff.views.modificar_staff'),
    url(r'^libreta_direcciones/$', 'direcciones.views.nueva_direccion'),
    url(r'^guardar_direccion_ajax/$', 'direcciones.views.guardar_direccion_ajax'),
    url(r'^locacion_ajax/$', 'evento.views.locacion_ajax'),
    url(r'^encargado_ajax/$', 'evento.views.encargado_ajax'),
    url(r'^sede_ajax/$', 'evento.views.sede_ajax'),
    url(r'^nuevo_cliente/$', 'clientes.views.nuevo_cliente'),
    url(r'^listar_cliente/$', 'clientes.views.listar_cliente'),
    url(r'^editar_cliente/(?P<id_cliente>\d+)/$', 'clientes.views.editar_cliente'),
    url(r'^eliminar_cliente/(?P<id_cliente>\d+)/$', 'clientes.views.eliminar_cliente'),
    url(r'^libreta_incluida/(?P<id_input>.*)$', 'direcciones.views.libreta_incluida'),
    url(r'^listar_evento/(?P<creado>\d+)/$', 'evento.views.listar_evento'),
    url(r'^nuevo_producto/$', 'productos.views.nuevo_producto'),
    url(r'^listar_producto/(?P<creado>\d+)/$', 'productos.views.listar_producto'),
    url(r'^editar_producto/(?P<id_producto>\d+)/$', 'productos.views.editar_producto'),
    url(r'^eliminar_producto/(?P<id_producto>\d+)/$', 'productos.views.eliminar_producto'),
   # url(r'^listar_pedidos_sede/(?P<id_producto>\d+)/$', 'productos.views.listar_pedidos_sede'),
    url(r'^exportar_csv_evento/$', 'modulo_movil.views.exportar_csv_evento'),
    url(r'^eliminar_direccion/$', 'direcciones.views.eliminar_direccion'),
    url(r'^agregar_staff/(?P<id_evento>\d+)/$', 'evento.views.agregar_staff'),
    url(r'^agregar_productos/(?P<id_evento>\d+)/$', 'evento.views.agregar_productos'),
    url(r'^casilla_administrativa/(?P<id_evento>\d+)/$', 'evento.views.casilla_administrativa'),
    url(r'^agregar_sede_macrocliente_ajax/$', 'clientes.views.agregar_sede_macrocliente_ajax'),
    url(r'^calendario_de_eventos/$', 'evento.views.calendario_de_eventos'),
    url(r'^regis_asistencia/$', 'evento.views.marcar_asistencia'),
    url(r'^usuario_por_evento/(?P<id_evento>\d+)/$', 'evento.views.usuario_por_evento'),
    url(r'^get_staff_usuario_por_evento/$', 'evento.views.get_staff_usuario_por_evento'),
    url(r'^get_staff_usuarios_usuario_por_evento/$', 'evento.views.get_staff_usuarios_usuario_por_evento'),
    url(r'^convocar_usuario_a_evento/$', 'evento.views.convocar_usuario_a_evento'),
    url(r'^crear_tarea/$', 'tareas.views.crear_tarea'),
    url(r'^editar_perfil/(?P<creado>\d+)/$', 'staff.views.editar_perfil'),
    url(r'^ver_perfil/(?P<id_staff>\d+)/$$', 'staff.views.ver_perfil'),
    url(r'^logout/$', 'staff.views.cerrar_sesion'),
    url(r'^nuevo_tipo_de_evento/(?P<creado>\d+)/$', 'evento.views.nuevo_tipo_de_evento'),
    url(r'^listar_tareas/$', 'tareas.views.listar_tareas'),
    url(r'^listar_todas_tareas/$', 'tareas.views.listar_todas_tareas'),
    url(r'^modificar_estado_tarea/$', 'tareas.views.modificar_estado_tarea'),
    url(r'^nuevo_tipo_de_evento/(?P<creado>\d+)/$', 'evento.views.nuevo_tipo_de_evento'),
    url(r'^ver_tarea/(?P<id_tarea>\d+)/$', 'tareas.views.ver_tarea'),
    url(r'^nueva_pauta/(?P<id_evento>\d+)/$', 'evento.views.nueva_pauta'),
    url(r'^editar_pauta/(?P<id_pauta>\d+)/$', 'evento.views.editar_pauta'),
    url(r'^eliminar_pauta/(?P<id_pauta>\d+)/$', 'evento.views.eliminar_pauta'),
    url(r'^crear_notificacion/$', 'tareas.views.crear_notificacion'),
    url(r'^listar_pautas/(?P<id_evento>\d+)/(?P<creado>\d+)/$', 'evento.views.listar_pautas'),
    url(r'^ver_pauta/(?P<id_pauta>\d+)/$', 'evento.views.ver_pauta'),
    url(r'^listar_notificaciones/$', 'tareas.views.listar_notificaciones'),
    url(r'^ver_notificacion/(?P<id_notificacion>\d+)/$', 'tareas.views.ver_notificacion'),
    url(r'^eliminar_notificacion/(?P<id_notificacion>\d+)/$', 'tareas.views.eliminar_notificacion'),
    url(r'^notificacion_marcar_como_leida/$', 'tareas.views.notificacion_marcar_como_leida'),
    url(r'^notificacion_marcar_como_no_leida/(?P<id_notificacion>\d+)/$', 'tareas.views.notificacion_marcar_como_no_leida'),
    url(r'^nueva_forma_de_pago/$', 'administracion.views.nueva_forma_de_pago'),
    url(r'^nuevo_tipo_de_gasto/$', 'administracion.views.nuevo_tipo_de_gasto'),
    url(r'^nuevo_gasto/$', 'administracion.views.nuevo_gasto'),
    url(r'^seleccionar_direccion/$', 'modulo_movil.views.selecccionar_direccion'),
    url(r'^crear_pedidos/(?P<id_evento>\d+)/(?P<next>[\w|\W]+)/urlseparador/(?P<actual>\w+)/$', 'modulo_movil.views.crear_pedidos'),
    url(r'^hacer_pago/$', 'administracion.views.pagar'),
    url(r'^crear_bloque/$', 'evento.views.crear_bloque'),
    url(r'^listar_bloques/(?P<id_bloque>\d+)/$', 'evento.views.listar_bloques'),
    url(r'^editar_bloque/(?P<id_bloque>\d+)/$', 'evento.views.editar_bloque'),
    url(r'^generar_pedido/(?P<pedido>\d+)/(?P<cedula>\d+)/$', 'modulo_movil.views.generar_pedido'),
    url(r'^ingresar_ticket/$', 'modulo_movil.views.ingresar_ticket'),
    url(r'^generar_lote/$', 'modulo_movil.views.generar_lote'),
    url(r'^agregar_item/$', 'modulo_movil.views.agregar_item'),
    url(r'^eliminar_productoeventopedido/(?P<id>\d+)/$', 'modulo_movil.views.eliminar_ProductoEventoPedido'),
    url(r'^eliminar_productoeventopedido_en_generarpedido/$', 'modulo_movil.views.eliminar_productoeventopedido_en_generarpedido'),
    url(r'^seleccionar_evento/$', 'modulo_movil.views.seleccionar_evento'),
    url(r'^edicion_lotes/$', 'productos.views.edicion_lotes'),
    url(r'^edicion_productos/(?P<pedido>\d+)/$', 'productos.views.edicion_productos'),
    url(r'^cambiar_estado_producto_edicion->editado/$', 'productos.views.cambiar_estado_producto_edicion_a_editado'),
    url(r'^edicion_pedido/(?P<lote>\d+)/$', 'productos.views.edicion_pedido'),
    url(r'^administrar_lotes/$', 'productos.views.administrar_lotes'),
    url(r'^administrar_pedidos/(?P<lote>\d+)/$', 'productos.views.administrar_pedidos'),
    url(r'^cambiar_estado_lotes_desde_administrar_pedidos/$', 'productos.views.cambiar_estado_lotes_desde_administrar_pedidos'),
    url(r'^generar_ticket/(?P<id_evento>\d+)/$', 'modulo_movil.views.generar_ticket'),
)
