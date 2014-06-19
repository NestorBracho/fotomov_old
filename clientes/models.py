from django.db import models
from marca.models import SubMarca
from direcciones.models import *

class MacroCliente(models.Model):
    submarca = models.ForeignKey(SubMarca)
    nombre = models.CharField(max_length=100, verbose_name="Nombre Institucion")
    telefono = models.CharField(max_length=100)
    rif = models.CharField(max_length=100, blank=True, null=True)
    direccion_fiscal = models.TextField(max_length=500)
    descripcion = models.TextField(max_length=1000, blank=True, null=True)
    def __unicode__(self):
        return '%s %s' % (self.submarca, self.nombre)  

class Encargado(models.Model):
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=8, blank=True, null=True)
    cargo = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=100)
    email = models.EmailField()
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    macrocliente = models.ForeignKey(MacroCliente)

class Cliente(models.Model):
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    telefono = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='correo electronico')
    direccion_fiscal = models.TextField(verbose_name='direccion fiscal', max_length=400)
    rif = models.CharField(max_length=10, null=True, blank=True)
    cedula = models.CharField(max_length=8, unique=True)
    def __unicode__(self):
        return '%s %s %s' % ( self.nombres, self.apellidos, self.cedula)

class Sede(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.ForeignKey(Direccion)
    macrocliente = models.ForeignKey(MacroCliente)