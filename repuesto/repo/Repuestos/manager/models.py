#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Vehiculo(models.Model):
  def __unicode__(self):
    return self.modelo
  usuario = models.ForeignKey(User)
  marca = models.CharField(max_length=100)
  modelo = models.CharField(max_length=100)
  year =  models.CharField(max_length=4)
  serial = models.CharField(max_length=100,null=True,blank=True)
  version = models.CharField(max_length=100,null=True,blank=True)

class Repuesto(models.Model):
  def __unicode__(self):
    return self.nombre
  vehiculo = models.ForeignKey(Vehiculo)
  nombre = models.CharField(max_length=100)
  numero = models.CharField(max_length=100,null=True,blank=True)
  #imagen = models.ImageField(upload_to='carga',null=True,blank=True)

class Pedido(models.Model):
  usuario = models.ForeignKey(User)
  vehiculo = models.ForeignKey(Vehiculo)
  repuesto = models.ForeignKey(Repuesto)
  precio = models.CharField(max_length=15,null=True,blank=True)
  marca = models.CharField(max_length=100,null=True,blank=True)
  status = models.CharField(max_length=100,null=True,blank=True)
  recibido = models.BooleanField()
  fecha = models.DateTimeField(auto_now=True)
  
class Telefono_Clientes(models.Model):
  user = models.ForeignKey(User)
  cod_telefono = models.CharField(max_length=4)
  telefono = models.CharField(max_length=7)
