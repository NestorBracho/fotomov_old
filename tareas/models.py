from django.db import models
from staff.models import *
from evento.models import *
from clientes.models import *
from administracion.models import *
# Create your models here.

class Tarea(models.Model):
    asignado = models.ForeignKey(Privilegios)
    original = models.IntegerField(null=True, blank=True)
    nombre = models.CharField(max_length=100)
    tarea = models.TextField(max_length=500)
    lista = models.CharField(max_length=100)
    evento = models.ForeignKey(Evento, null=True, blank=True)
    fecha = models.DateField()
    fecha_activacion =  models.DateField(null=True, blank=True)
    fecha_realizacion =  models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=False)
    es_periodica = models.BooleanField(default=False)
    fue_hecha = models.BooleanField(default=False)

class Prela(models.Model):
    es_prelada = models.ForeignKey(Tarea, related_name="es_prelada")
    prela = models.ForeignKey(Tarea)

class TareaTipoEvento(models.Model):
    asignado = models.ForeignKey(Privilegios)
    nombre = models.CharField(max_length=100)
    tarea = models.TextField(max_length=500)
    tipo_evento = models.ForeignKey(Tipos_Eventos)
    dias = models.IntegerField()
    id_aux = models.TextField(max_length=5, null=True, blank=True)

class PrelaTareaTipoEvento(models.Model):
    es_prelada = models.ForeignKey(TareaTipoEvento, related_name="es_prelada_tipo_evento")
    prela = models.ForeignKey(TareaTipoEvento)
    tipo_evento = models.ForeignKey(Tipos_Eventos)

class Notificacion(models.Model):
    choices_tipo= (('N/A', 'N/A'), ('Queja', 'Queja'), ('Sugerencia', 'Sugerencia'))
    macro_cliente = models.ForeignKey(MacroCliente, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    usuario_creador = models.ForeignKey(Usuario)
    creado_fecha = models.DateTimeField(auto_now_add=True)
    notificacion = models.TextField(max_length=500)
    fue_revisado = models.BooleanField(default = False)
    tipo = models.CharField(max_length=15, choices=choices_tipo, default=None)