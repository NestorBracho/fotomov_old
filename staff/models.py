from django.db import models
from django.contrib.auth.models import User

class Privilegios(models.Model):
  valor = models.IntegerField()
  nombre = models.TextField(max_length=60,unique=True)
  def __unicode__(self):
      return self.nombre

class Usuario(models.Model):
  usuario = models.ForeignKey(User,unique=True)
  nombre = models.CharField(max_length=60)
  apellido = models.CharField(max_length=60)
  cedula = models.CharField(max_length=60,unique=True)
  email = models.EmailField(max_length=100)
  privilegio = models.ForeignKey(Privilegios)
  equipos = models.CharField(max_length=1000, null=True, blank=True)

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


