from django.db import models
from evento.models import Funcion
from django.contrib.auth.models import User
from productos.models import *

class direccionFuncion(models.Model):
    funcion = models.ForeignKey(Funcion)
    dir = models.CharField(max_length=10000)

class direcciones_exportacion(models.Model):
    ruta = models.CharField(max_length=1000)

class directorio_actual(models.Model):
    usuario = models.ForeignKey(User)
    directorio = models.CharField(max_length=10000)
    pedido = models.ForeignKey(Pedido)

class cliente_aux(models.Model):
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    telefono = models.CharField(max_length=11)
    email = models.EmailField(verbose_name='correo electronico')
    direccion_fiscal = models.TextField(verbose_name='direccion fiscal', max_length=400)
    rif = models.CharField(max_length=10, null=True, blank=True)
    cedula = models.CharField(max_length=8, null=True, blank=True)
    def __unicode__(self):
        return self.nombres+" "+self.apellidos

class pedido_aux(models.Model):
    cliente = models.ForeignKey(cliente_aux, null=True, blank=True)
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
    envio = models.BooleanField(default=False)
    fue_pagado = models.BooleanField(default=False)
    lote = models.ForeignKey(Lote, null=True, blank=True)
    estado = models.CharField(max_length=100)

class ProductoEventoPedido_aux(models.Model):
    cantidad = models.IntegerField()
    ruta = models.CharField(max_length=10000)
    num_pedido = models.IntegerField()
    producto = models.IntegerField()
    estado = models.CharField(max_length=50)
    comentario = models.TextField(max_length=1000)

class PedidoPago_aux(models.Model):
    num_pedido = models.IntegerField()
    tipo_pago = models.IntegerField()
    monto = models.FloatField()
    referencia = models.CharField(max_length=100)


class Configuracion(models.Model):
    nombre = models.CharField(max_length=30)
    valor = models.DecimalField(decimal_places=0, max_digits=5)