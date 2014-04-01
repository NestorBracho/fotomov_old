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

#@login_required(login_url='/')
#def crear_pedidos(request, id_evento, next, actual):
#    print next
#    #print directorio_actual.objects.filter(usuario = request.user)
#    if directorio_actual.objects.filter(usuario = request.user):
#        dir_actual = directorio_actual.objects.get(usuario=request.user)
#    else:
#        dir_actual = directorio_actual.objects.create(usuario=request.user, directorio = settings.MEDIA_ROOT + "/eventos/")
#    evento = Evento.objects.get(id=id_evento)
#    funciones = Funcion.objects.filter(evento=evento)
#    generar_rutas(id_evento)
#    print "aqui"
#    print dir_actual.directorio
#    separado = request.path.split('urlseparador')
#    print separado
#    year = str(date.today().year)
#    if actual == "NoneValue":
#        print "NoneValue"
#        current = dir_actual.directorio
#    elif actual == "ir":
#        split_auxiliar = next.split(" ")
#        print len(split_auxiliar)
#        if len(split_auxiliar) > 1:
#            print "entre"
#            i=0
#            concatenar = ""
#            while i < len(split_auxiliar) - 1:
#                concatenar = concatenar + split_auxiliar[i] + "\"
#                i = i + 1
#            next = concatenar
#            print "el nuevo next es =" + next
#        auxiliar = dir_actual.directorio
#        dir_actual.directorio = auxiliar + next + "/"
#        dir_actual.save()
#        current = dir_actual.directorio
#    elif actual == "back":
#        auxiliar = dir_actual.directorio.split("/")
#        i = 0
#        print "antes del while"
#        concatenar = ""
#        while i < len(auxiliar) - 2:
#            if i == 0:
#                concatenar = concatenar + auxiliar[i]
#            else:
#                concatenar = concatenar + "/" + auxiliar[i]
#            print auxiliar[i]
#            i= i + 1
#        dir_actual.directorio = concatenar + "/"
#        dir_actual.save()
#        current = dir_actual.directorio
#    else:
#        print "estoy en el else"
#        current = settings.MEDIA_ROOT + "/eventos/" + year + "" + separado[1]
#        print "sali del else"
#    print "aqui va el current"
#    print current
#    short_current = current.split("fotomov_imagenes")[1]
#    print "aqui va el short"
#    print short_current
#    lista_imagenes = []
#    imagenes = [ f for f in listdir(current) if isfile(join(current,f)) ]
#    for imagen in imagenes:
#        dividir_url = imagen.split("fotomov_imagenes")
#    directorios = [ f for f in listdir(current) if isdir(join(current,f)) ]
#    print imagenes
#    print directorios
#    if request.method == 'POST':
#        pass
#    return render_to_response('modulo_movil/crear_pedidos.html', {'imagenes': imagenes, 'directorios': directorios, 'current': current, 'evento': evento, 'short_current': short_current}, context_instance=RequestContext(request))

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