from staff.models import Usuario
from django.contrib import admin
from staff.models import *
from clientes.models import *
from evento.models import *
from productos.models import *

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
admin.site.register(ProductoFuncion)
admin.site.register(ProductoFuncionPedido)
admin.site.register(ProductoImpresion)