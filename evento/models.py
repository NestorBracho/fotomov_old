from django.db import models
from clientes.models import Encargado
from direcciones.models import Direccion
from clientes.models import Sede
#encoding:utf-8

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000)
    porcentaje_institucion = models.FloatField()
    encargado = models.ForeignKey(Encargado)
    locacion = models.ManyToManyField(Sede)

class Funcion(models.Model):
    horas = models.IntegerField(max_length=2)
    entrega_fotos = models.DateField()
    sede = models.ForeignKey(Sede)

class Gasto(models.Model):
    nombre = models.CharField(max_length=100)
    predeterminado = models.BooleanField()

class Gastos_Funcion(models.Model):
    monto = models.FloatField()
    gasto = models.ForeignKey(Gasto)
    funcion = models.ForeignKey(Funcion)

