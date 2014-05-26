from django.db import models
from tareas.models import *
from staff.models import *
from evento.models import *
from productos.models import *

class TipoDeGasto(models.Model):
    nombre = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nombre

class GastoAdministracion(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoDeGasto)
    forma_de_pago = models.ForeignKey(FormaDePago)
    monto = models.FloatField()
    moneda = models.CharField(max_length=100, null=True, blank=True, default = None)
    frecuencia = models.IntegerField()
    intervalos_dias = models.IntegerField()
    def __unicode__(self):
        return self.nombre

class GastoEvento(models.Model):
    nombre = models.CharField(max_length=100)
    monto = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    tipo = models.IntegerField(null=True, blank=True, verbose_name="1-fijo 2-envio 3-adicional")
    fue_pagado = models.BooleanField(default=False)
    productos = models.ForeignKey(ProductoEvento, null=True, blank=True, verbose_name="Producto asociado")
    usuario = models.ForeignKey(Usuario, null=True, blank=True, verbose_name="Honorarios")
    funcion = models.ForeignKey(Funcion, null=True, blank=True, verbose_name="Si esta asociado a una funcion")
    evento = models.ForeignKey(Evento, null=True, blank=True, verbose_name="Evento relacionado")
    def __unicode__(self):
        return self.nombre

class Pago(models.Model):
    pago = models.TextField(max_length=500)
    forma_de_pago = models.ForeignKey(FormaDePago)
    monto = models.FloatField()
    fecha_de_pago = models.DateField()
    banco = models.CharField(max_length=100)
    nro_de_comprobante = models.CharField(max_length=100)
    gasto = models.ForeignKey(GastoEvento, null=True, blank=True)
    def __unicode__(self):
        return self.pago