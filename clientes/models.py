from django.db import models
from marca.models import SubMarca

class MacroCliente(models.Model):
    submarca = models.ForeignKey(SubMarca)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=11)
    rif = models.CharField(max_length=10)
    direccion_fiscal = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=400)

class Direccion(models.Model):
    direccion = models.CharField(max_length=500)
    lon = models.FloatField()
    lat = models.FloatField()
    descripcion = models.CharField(max_length=500)
    macrocliente = models.ForeignKey(MacroCliente)

class Encargado(models.Model):
    nombre = models.CharField(max_length=100)
    ceula = models.CharField(max_length=8)
    telefono = models.CharField(max_length=11)
    email = models.EmailField()
    descripcion = models.CharField(max_length=500)
    macrocliente = models.ForeignKey(MacroCliente)



