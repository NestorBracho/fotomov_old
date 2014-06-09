from django.db import models
from clientes.models import *
from evento.models import *

class FormaDePago(models.Model):
    nombre = models.CharField(max_length=100)
    descuento = models.BooleanField(default=True)
    pagado = models.BooleanField(default=True)
    def __unicode__(self):
        return self.nombre

class Lote(models.Model):
    estado = models.CharField(max_length=100)
    fecha = models.DateField(auto_now=True)
    ruta = models.CharField(max_length=10000)
    codigo = models.CharField(max_length=100)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=400)
    es_combo = models.BooleanField(default=False)
    def __unicode__(self):
        return self.nombre

class ProductoEvento(models.Model):
    precio = models.FloatField()
    precio_produccion = models.FloatField()
    es_combo = models.BooleanField(default=False)

    #Claves foraneas
    evento = models.ForeignKey(Evento)
    producto = models.ForeignKey(Producto)
    def __unicode__(self):
        return self.producto.nombre

class ProductoImpresion(models.Model):
    precio = models.FloatField()

class ProductoEventoPedido(models.Model):
    cantidad = models.IntegerField()
    ruta = models.CharField(max_length=10000)
    num_pedido = models.IntegerField()
    estado = models.CharField(max_length=50, default='Creado')
    comentario = models.TextField(max_length=1000)

    #Claves foraneas
    producto = models.ForeignKey(ProductoEvento)

class Pedido(models.Model):
    fecha = models.DateField(auto_now=True)
    num_pedido= models.IntegerField()
    fecha_entrega = models.DateField(null=True, blank=True)
    id_fiscal = models.CharField(max_length=100, null=True, blank=True)
    direccion_fiscal = models.TextField(max_length=400, null=True, blank=True)
    tlf_fiscal = models.CharField(max_length=11, null=True, blank=True)
    razon_social = models.CharField(max_length=200, null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    codigo = models.CharField(max_length=100, null=True, blank=True)
    direccion_entrega = models.TextField(max_length=400, null=True, blank=True)
    envio = models.IntegerField(default=0)
    fue_pagado = models.BooleanField(default=False)
    estado = models.CharField(max_length=100)
    factura = models.BooleanField(default=False)

    #Claves foraneas
    cliente = models.ForeignKey(Cliente, null=True, blank=True)
    lote = models.ForeignKey(Lote, null=True, blank=True)

class PedidoPago(models.Model):
    num_pedido = models.IntegerField()
    monto = models.FloatField()
    referencia = models.CharField(max_length=100)

    #Claves foraneas
    tipo_pago = models.ForeignKey(FormaDePago)

class ProductoeventoCombo(models.Model):#tabla de rompimiento entre ProductoEvento y Combos
    cantidad = models.IntegerField()

    #Claves foraneas
    producto = models.ForeignKey(ProductoEvento, related_name='producto_r')
    combo = models.ForeignKey(ProductoEvento, related_name='combo')