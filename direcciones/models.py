from django.db import models

class Direccion(models.Model):
    nombre = models.CharField(max_length=200, unique=True, blank=False)
    direccion = models.CharField(max_length=500)
    lon = models.FloatField()
    lat = models.FloatField()
    es_sede = models.BooleanField(default=False)
    descripcion = models.CharField(max_length=500)