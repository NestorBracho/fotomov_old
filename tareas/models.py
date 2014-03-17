from django.db import models
from staff.models import Privilegios, Usuario
from evento.models import *
# Create your models here.

class Tarea(models.Model):
    asignado = models.ForeignKey(Privilegios)
    nombre = models.CharField(max_length=100)
    tarea = models.TextField(max_length=500)
    lista = models.BooleanField(default=False)
    evento = models.ForeignKey(Evento)
    dias = models.IntegerField()
    fecha = models.DateField()

class Prela(models.Model):
    es_prelada = models.ForeignKey(Tarea, related_name="es_prelada")
    prela = models.ForeignKey(Tarea)