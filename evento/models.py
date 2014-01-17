from django.db import models
#encoding:utf-8

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000)

class Direccion(models.Model):
    direccion = models.CharField(max_length=1000)
    lon = models.CharField(max_length=30)
    lat = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=1000)

class Sede(models.Model):
    fecha = models.DateField()
    direccion = models.ForeignKey(Direccion)


