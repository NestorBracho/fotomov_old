from django.db import models

class Pedido(models.Model):
    fecha = models.DateField()
    fecha_entrega = models.DateField()
    id_fiscal = models.CharField(max_length=100)
    direccion_fiscal = models.TextField(max_length=400)
    tlf_fiscal = models.CharField(max_length=11)
    razon_fiscal = models.CharField(max_length=200)
    total = models.FloatField()
    codigo = models.CharField(max_length=100)
    direccion_entrega = models.TextField(max_length=400)
    envio = models.BooleanField()

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=400)

class ProductoFuncion(models.Model):
    precio = models.FloatField()

class ProductoImpresion(models.Model):
    precio = models.FloatField()

class ProductoFuncionPedido(models.Model):
    cantidad = models.IntegerField()
    ruta = models.CharField(max_length=600)
    producto = models.ForeignKey(ProductoFuncion)
    pedido = models.ForeignKey(Pedido)
