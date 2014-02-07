from staff.models import Usuario
from django.contrib import admin
from staff.models import *
from clientes.models import *
from evento.models import *

admin.site.register(Usuario)
admin.site.register(Privilegios)
admin.site.register(Direccion)
admin.site.register(MacroCliente)
admin.site.register(Funcion)
admin.site.register(Gasto)
admin.site.register(TipoStaff)