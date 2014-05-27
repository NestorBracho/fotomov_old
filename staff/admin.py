from staff.models import Usuario
from django.contrib import admin
from staff.models import *
from clientes.models import *
from evento.models import *
from productos.models import *
from tareas.models import *
from administracion.models import *
from modulo_movil.models import *


admin.site.register(Usuario)
admin.site.register(Privilegios)
admin.site.register(Direccion)
admin.site.register(MacroCliente)
admin.site.register(Funcion)
admin.site.register(Gasto)
admin.site.register(Encargado)
admin.site.register(Sede)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(ProductoEvento)
admin.site.register(ProductoEventoPedido)
admin.site.register(ProductoImpresion)
admin.site.register(Evento)
admin.site.register(StaffPorFuncion)
admin.site.register(AsistenciaStaffFuncion)
admin.site.register(Equipos)
admin.site.register(Experiencia)
admin.site.register(DatoDePago)
admin.site.register(Tarea)
admin.site.register(TareaTipoEvento)
admin.site.register(Tipos_Eventos)
admin.site.register(PrelaTareaTipoEvento)
admin.site.register(Notificacion)
admin.site.register(Prela)
admin.site.register(FormaDePago)
admin.site.register(TipoDeGasto)
admin.site.register(GastoAdministracion)
admin.site.register(Pago)
admin.site.register(direccionFuncion)
admin.site.register(Bloque)
admin.site.register(directorio_actual)
admin.site.register(Lote)
admin.site.register(cliente_aux)
admin.site.register(pedido_aux)
admin.site.register(ProductoEventoPedido_aux)
admin.site.register(GastoEvento)
admin.site.register(ProductoeventoCombo)
admin.site.register(PedidoPago)
admin.site.register(Configuracion)