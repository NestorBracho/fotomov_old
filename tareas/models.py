from django.db import models
from staff.models import Privilegios, Usuario
# Create your models here.

class Tarea(models.Model):
    asignado = models.ForeignKey(Privilegios)
    tarea = models.TextField(max_length=500)
    lista = models.BooleanField(default=False)
    privada = models.ForeignKey(Tarea, null=True, blank=True)