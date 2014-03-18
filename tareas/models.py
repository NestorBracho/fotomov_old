from django.db import models
from staff.models import Privilegios, Usuario
from evento.models import *
# Create your models here.

class Tarea(models.Model):
    asignado = models.ForeignKey(Privilegios)
    nombre = models.CharField(max_length=100)
    tarea = models.TextField(max_length=500)
    lista = models.BooleanField(default=False)
    evento = models.ForeignKey(Evento, null=True, blank=True)
    fecha = models.DateField()

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