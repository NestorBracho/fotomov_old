from django.db import models

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
    fecha_de_pago = models.DateField()
    def __unicode__(self):
        return self.nombre

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