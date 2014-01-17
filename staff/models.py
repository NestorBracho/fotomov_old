from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
  usuario = models.ForeignKey(User,unique=True)
  nombre = models.CharField(max_length=60)
  apellido = models.CharField(max_length=60)
  cedula = models.CharField(max_length=60,unique=True)
  privilegio = models.IntegerField()

class Notificacion(models.Model):
  categoria = models.TextField()
  mensaje = models.TextField()
  fecha_creado = models.DateField(auto_now=True)
  hora = models.DateTimeField(auto_now=True)
  realizado = models.BooleanField()
  fecha_asignacion = models.DateField()
