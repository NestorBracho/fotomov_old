from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique= True)
    def __unicode__(self):
        return self.nombre

class SubMarca(models.Model):
    nombre = models.CharField(max_length=100)

    #Claves foraneas
    marca = models.ForeignKey(Marca)
    def __unicode__(self):
        return self.nombre