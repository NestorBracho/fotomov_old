import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from staff.models import *
from tareas.models import *
from tareas.forms import *
import datetime

def crear_tarea(request):
    eventos = Evento.objects.all()
    error_fecha = 0
    if request.method == 'POST':
        formulario = TareaForm(request.POST)
        fecha = request.POST.get('fecha')
        if fecha == "":
            error_fecha = 1
            return render_to_response('tareas/crear_tarea.html', {'formulario': formulario, 'eventos': eventos, 'error_fecha': error_fecha}, context_instance=RequestContext(request))
        if formulario.is_valid():
            fecha_split= fecha.split('-')
            fecha_final= fecha_split[2] + "-" + fecha_split[1] + "-" + fecha_split[0]
            evento = request.POST.get('evento')
            if evento == None:
                tarea = Tarea.objects.create(asignado=formulario.cleaned_data['asignado'], nombre=formulario.cleaned_data['nombre'], tarea=formulario.cleaned_data['tarea'],
                                             lista=False, fecha=fecha_final)
            else:
                tarea = Tarea.objects.create(asignado=formulario.cleaned_data['asignado'], nombre=formulario.cleaned_data['nombre'], tarea=formulario.cleaned_data['tarea'],
                                             lista=False, fecha=fecha_final, evento=Evento.objects.get(id=evento))

    else:
        formulario = TareaForm()
    return render_to_response('tareas/crear_tarea.html', {'formulario': formulario, 'eventos': eventos, 'error_fecha': error_fecha}, context_instance=RequestContext(request))

def ver_tarea(request, id_tarea):
    tarea = Tarea.objects.get(id=id_tarea)
    prela = Prela.objects.filter(prela=tarea)
    es_prelada = Prela.objects.filter(es_prelada=tarea)
    return render_to_response('tareas/ver_tarea.html', {'tarea':tarea, 'prela':prela, 'es_prelada': es_prelada}, context_instance=RequestContext(request))
