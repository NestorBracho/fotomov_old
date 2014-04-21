from django.db import models
from evento.models import Funcion
from django.contrib.auth.models import User
from productos.models import Pedido

class direccionFuncion(models.Model):
    funcion = models.ForeignKey(Funcion)
    dir = models.CharField(max_length=10000)

class direcciones_exportacion(models.Model):
    ruta = models.CharField(max_length=1000)

class directorio_actual(models.Model):
    usuario = models.ForeignKey(User)
    directorio = models.CharField(max_length=10000)
    pedido = models.ForeignKey(Pedido)

