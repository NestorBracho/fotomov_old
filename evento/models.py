from django.db import models
from clientes.models import Encargado
from direcciones.models import Direccion
from clientes.models import Sede
#encoding:utf-8
class Tipos_Eventos(models.Model):
    nombre = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000)
    porcentaje_institucion = models.FloatField()
    encargado = models.ForeignKey(Encargado)
    sede = models.ForeignKey(Sede, null=True)
    tipo = models.ForeignKey(Tipos_Eventos, verbose_name="Tipo de evento")

class Funcion(models.Model):
    nombre = models.CharField(max_length=200)
    evento = models.ForeignKey(Evento)
    dia = models.DateField()
    horas = models.IntegerField(max_length=2, null=True, blank=True)
    entrega_fotos = models.CharField(max_length=20)
    direccion = models.ForeignKey(Direccion)


class Gasto(models.Model):
    nombre = models.CharField(max_length=100)
    predeterminado = models.BooleanField()

class Gastos_Funcion(models.Model):
    monto = models.FloatField()
    gasto = models.ForeignKey(Gasto)
    funcion = models.ForeignKey(Funcion)

class Pautas(models.Model):
    evento = models.ForeignKey(Evento)
    nombre = models.CharField(max_length=300)
    pauta = models.TextField(max_length=2000)
    fecha = models.DateField(auto_now=True)
