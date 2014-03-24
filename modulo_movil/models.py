from django.db import models
from evento.models import Funcion

class direccionFuncion(models.Model):
    funcion = models.ForeignKey(Funcion)
    dir = models.CharField(max_length=1000)

class direcciones_exportacion(models.Model):
    ruta = models.CharField(max_length=1000)