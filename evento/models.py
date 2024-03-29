from django.db import models
from clientes.models import Encargado
from direcciones.models import Direccion
from clientes.models import Sede, MacroCliente, Cliente
from marca.models import SubMarca
#encoding:utf-8
class Tipos_Eventos(models.Model):
    nombre = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000)
    porcentaje_institucion = models.FloatField()

    #Claves foraneas
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    encargado = models.ForeignKey(Encargado,null=True, blank=True)
    sede = models.ForeignKey(Sede, null=True, blank=True)
    macrocliente = models.ForeignKey(MacroCliente, blank=True, null=True)
    fecha_entrega = models.DateField()
    tipo = models.ForeignKey(Tipos_Eventos, verbose_name="Tipo de evento")
    submarca = models.ForeignKey(SubMarca)

class Funcion(models.Model):
    nombre = models.CharField(max_length=200)
    dia = models.DateField()
    horas = models.IntegerField(max_length=2, null=True, blank=True)
    entrega_fotos = models.CharField(max_length=20)
    
    #Claves foraneas
    evento = models.ForeignKey(Evento)
    direccion = models.ForeignKey(Direccion)

class Gasto(models.Model):
    nombre = models.CharField(max_length=100)
    predeterminado = models.BooleanField()

class Gastos_Funcion(models.Model):
    monto = models.FloatField()

    #Claves foraneas
    gasto = models.ForeignKey(Gasto)
    funcion = models.ForeignKey(Funcion)

class Pautas(models.Model):
    nombre = models.CharField(max_length=300)
    pauta = models.TextField(max_length=2000)
    fecha = models.DateField(auto_now=True)

    #Claves foraneas
    evento = models.ForeignKey(Evento)
    
class Bloque(models.Model):
    nombre = models.CharField(max_length=100)
    honorarios = models.FloatField()
    unico = models.BooleanField()
    def __unicode__(self):
        return self.nombre