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
import os
from os.path import exists
from os import makedirs
from django.conf import settings

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

def crear_pedidos(request, id_evento):
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    print generar_rutas(id_evento)
    return render_to_response('modulo_movil/crear_pedidos.html', {}, context_instance=RequestContext(request))

def generar_rutas(id_evento):
    lista = []
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    for funcion in funciones:
        direccion = direccionFuncion.objects.get(funcion=funcion)
        ruta = settings.MEDIA_ROOT + '/' + direccion.dir
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        print ruta
        lista.append(ruta)
    return lista