from django.db import models
from django.contrib.auth.models import User
from evento.models import Funcion


class Privilegios(models.Model):
  valor = models.IntegerField()
  nombre = models.TextField(max_length=60,unique=True)
  def __unicode__(self):
      return self.nombre

class Equipos(models.Model):
    marca = models.CharField(max_length=300, verbose_name="Marca y modelo de camara", null=True, blank=True)
    flash = models.CharField(max_length=300, verbose_name="Flash externo (modelo)", null=True, blank=True)
    lente_1 = models.CharField(max_length=300, verbose_name="Lente 1", null=True, blank=True)
    lente_2 = models.CharField(max_length=300, verbose_name="Lente 2", null=True, blank=True)
    lente_3 = models.CharField(max_length=300, verbose_name="Lente 3", null=True, blank=True)
    memorias = models.CharField(max_length=300, verbose_name="# Tarjetas de memoria y capacidad", null=True, blank=True)
    iluminacion = models.CharField(max_length=300, verbose_name="Iluminacion Profesional", null=True, blank=True)
    otros = models.CharField(max_length=300, verbose_name="Otros (tripoide, sinfin, portasinfin)", null=True, blank=True)

class Experiencia(models.Model):
    lightroom = models.IntegerField(verbose_name="Manejo de Lightroom/Nivel (del 1 al 10)", null=True, blank=True)
    photoshop = models.IntegerField(verbose_name="Manejo de Photoshop/Nivel (del 1 al 10)", null=True, blank=True)
    tipos = models.TextField(verbose_name="Tipo de eventos donde ha trabajo. Especialidad", max_length=400, null=True, blank=True)

class DatoDePago(models.Model):
    banco = models.CharField(max_length=100, verbose_name="Banco", null=True, blank=True)
    tipo_de_cuenta = models.CharField(max_length=100, verbose_name="Tipo de cuenta", null=True, blank=True)
    numero = models.CharField(max_length=100, verbose_name="Numero de cuenta", null=True, blank=True)

class Usuario(models.Model):
    nombre = models.CharField(max_length=60, null=True, blank=True)
    apellido = models.CharField(max_length=60, null=True, blank=True)
    cedula = models.CharField(max_length=60, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=11, null=True, blank=True)
    telefono_celular = models.CharField(max_length=11, null=True, blank=True)
    telefono_otro = models.CharField(max_length=11, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    usuario = models.ForeignKey(User,unique=True)
    privilegio = models.ForeignKey(Privilegios)
    equipos = models.ForeignKey(Equipos, null=True, blank=True)
    experiencia = models.ForeignKey(Experiencia, null=True, blank=True)
    datos_pago = models.ForeignKey(DatoDePago, null=True, blank=True)

class TipoStaff(models.Model):
  nombre = models.CharField(max_length=100)
  descripcion = models.CharField(max_length=1000)
  def __unicode__(self):
      return self.nombre

class Notificacion(models.Model):
  categoria = models.TextField()
  mensaje = models.TextField()
  fecha_creado = models.DateField(auto_now=True)
  hora = models.DateTimeField(auto_now=True)
  realizado = models.BooleanField()
  fecha_asignacion = models.DateField()

class StaffPorFuncion(models.Model):
    tipo = models.ForeignKey(Privilegios)
    funcion = models.ForeignKey(Funcion)
    cantidad = models.IntegerField()

class AsistenciaStaffFuncion(models.Model):
    funcion = models.ForeignKey(Funcion)
    usuario = models.ForeignKey(Usuario)
    asistencia = models.BooleanField(default = False)
    fue_convocado = models.BooleanField(default = False)
    email_enviado = models.BooleanField(default = False)
