from django.db import models
from staff.models import Privilegios, Usuario
# Create your models here.

class Tarea(models.Model):
    asignado = models.ForeignKey(Privilegios)
    nombre = models.CharField(max_length=100)
    tarea = models.TextField(max_length=500)
    lista = models.BooleanField(default=False)


class Prela(models.Model):
    es_prelada = models.ForeignKey(Tarea, related_name="es_prelada")
    prela = models.ForeignKey(Tarea)