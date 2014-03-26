from django.db import models
from tareas.models import *

class FormaDePago(models.Model):
    nombre = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nombre

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

class Pago(models.Model):
    gasto = models.ForeignKey(GastoAdministracion)
    forma_de_pago = models.ForeignKey(FormaDePago)
    monto = models.FloatField()
    frecuencia_de_pago = models.IntegerField()
    fehca_de_pago = models.IntegerField()
    banco = models.CharField(max_length=100)
    nro_de_comprobante = models.IntegerField()