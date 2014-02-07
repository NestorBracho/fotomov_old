from django.db import models
from marca.models import SubMarca

class MacroCliente(models.Model):
    submarca = models.ForeignKey(SubMarca)
    nombre = models.CharField(max_length=100, verbose_name="Nombre Institucion")
    telefono = models.CharField(max_length=11)
    rif = models.CharField(max_length=10, unique=True)
    direccion_fiscal = models.TextField(max_length=500)
    descripcion = models.TextField(max_length=1000, blank=True, null=True)
    def __unicode__(self):
        return self.nombre

class Direccion(models.Model):
    direccion = models.CharField(max_length=500)
    lon = models.FloatField()
    lat = models.FloatField()
    descripcion = models.CharField(max_length=500)
    macrocliente = models.ForeignKey(MacroCliente)

class Encargado(models.Model):
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=8, unique=True, blank=True, null=True)
    cargo = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=11)
    email = models.EmailField()
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    macrocliente = models.ForeignKey(MacroCliente)



