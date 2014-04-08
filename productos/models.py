from django.db import models
from clientes.models import *
from evento.models import *

class Lote(models.Model):
    estado = models.CharField(max_length=100)
    fecha = models.DateField(auto_now=True)
    ruta = models.CharField(max_length=10000)
    codigo = models.CharField(max_length=100)

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    fecha = models.DateField(auto_now=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    id_fiscal = models.CharField(max_length=100, null=True, blank=True)
    direccion_fiscal = models.TextField(max_length=400, null=True, blank=True)
    tlf_fiscal = models.CharField(max_length=11, null=True, blank=True)
    razon_social = models.CharField(max_length=200, null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    codigo = models.CharField(max_length=100, null=True, blank=True)
    direccion_entrega = models.TextField(max_length=400, null=True, blank=True)
    envio = models.BooleanField(default=False)
    fue_pagado = models.BooleanField(default=False)
    lote = models.ForeignKey(Lote, null=True, blank=True)
    estado = models.CharField(max_length=100)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=400)
    def __unicode__(self):
        return self.nombre

class ProductoEvento(models.Model):
    evento = models.ForeignKey(Evento)
    producto = models.ForeignKey(Producto)
    precio = models.FloatField()
    def __unicode__(self):
        return self.producto.nombre

class ProductoImpresion(models.Model):
    precio = models.FloatField()

class ProductoEventoPedido(models.Model):
    cantidad = models.IntegerField()
    ruta = models.CharField(max_length=10000)
    num_pedido = models.IntegerField()
    producto = models.ForeignKey(ProductoEvento)
    pedido = models.ForeignKey(Pedido, null=True, blank=True)
    estado = models.CharField(max_length=50)
    comentario = models.TextField(max_length=1000)
