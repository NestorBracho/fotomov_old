from django.db import models
from evento.models import Funcion

class direcciones_exportacion:
    ruta = models.CharField(max_length=1000)