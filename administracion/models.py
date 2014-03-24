from django.db import models

class FormaDePago(models.Model):
    nombre = models.CharField(max_length=100)

class TipoDeGasto(models.Model):
    nombre = models.CharField(max_length=100)

class GastoAdministracion(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoDeGasto)
    forma_de_pago = models.ForeignKey(FormaDePago)
    monto = models.FloatField()
    moneda = models.CharField(max_length=100)
    fecha_de_pago = models.DateField()

class Pago(models.Model):
    gasto = models.ForeignKey(GastoAdministracion)
    forma_de_pago = models.ForeignKey(FormaDePago)
    monto = models.FloatField()
    fehca_de_pago = models.DateField()
    banco = models.CharField(max_length=100)
    nro_de_comprobante = models.IntegerField()

class RecordatorioPago(models.Model):
    pago = models.ForeignKey(Pago)
    fecha_recordatorio = models.DateField()
    nota_recordatorio = models.CharField(max_length=500)