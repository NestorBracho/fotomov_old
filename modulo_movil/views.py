from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from evento.forms import *
from modulo_movil.models import *
from evento.models import *
import csv
import time
from datetime import date
import os
from os.path import exists
from os import makedirs
from django.conf import settings
from os import listdir
from os.path import isfile, join, isdir

def exportar_csv_evento(request):
    eventos = Evento.objects.all().order_by('-id')
    if request.method == 'POST':
        pass
       # exportar = request.POST.getlist('eventos')
       # nombre = "BDD-" + time.strftime("%d/%m/%Y") + ".csv"
       # archivo = open(nombre,"w+")
       # print nombre
    else:
        pass
    return render_to_response('modulo_movil/exportar_csv_evento.html', {'eventos': eventos},
                              context_instance=RequestContext(request))

def selecccionar_direccion(request):
#    print settings.MEDIA_ROOT
#    settings.MEDIA_ROOT = '/home/leonardo/turpial'
#    print settings.MEDIA_ROOT
    if request.method == 'POST':
        directorio = request.POST.get('directorio')
        settings.MEDIA_ROOT = directorio
        print settings.MEDIA_ROOT
        return HttpResponseRedirect('/escritorio')
    return render_to_response('modulo_movil/seleccionar_directorio.html', {}, context_instance=RequestContext(request))

def crear_pedidos(request, id_evento, next):
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    generar_rutas(id_evento)
    print "aqui"
    print request.path
    separado = request.path.split('urlseparador')
    print separado
    year = str(date.today().year)
    if separado[1] == "/NoneValue":
        print separado
        current = settings.MEDIA_ROOT + "/eventos/"
    else:
        print "estoy en el else"
        current = settings.MEDIA_ROOT + "/eventos/" + year + "" + separado[1]
        print "sali del else"
    print "aqui va el current"
    print current
    short_current = current.split("fotomov_imagenes")[1]
    print "aqui va el short"
    print short_current
    lista_imagenes = []
    imagenes = [ f for f in listdir(current) if isfile(join(current,f)) ]
    for imagen in imagenes:
        dividir_url = imagen.split("fotomov_imagenes")
    directorios = [ f for f in listdir(current) if isdir(join(current,f)) ]
    print imagenes
    print directorios
    if request.method == 'POST':
        pass
    return render_to_response('modulo_movil/crear_pedidos.html', {'imagenes': imagenes, 'directorios': directorios, 'current': current, 'evento': evento, 'short_current': short_current}, context_instance=RequestContext(request))

def generar_rutas(id_evento):
    lista = []
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    year = str(date.today().year)

    for funcion in funciones:
        direccion = direccionFuncion.objects.get(funcion=funcion)
        ruta = settings.MEDIA_ROOT + "/eventos/" + year + '/' + direccion.dir
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        #print ruta
        lista.append(ruta)
    return lista