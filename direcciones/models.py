from django.db import models

class Direccion(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=500)
    lon = models.FloatField()
    lat = models.FloatField()
    descripcion = models.CharField(max_length=500)