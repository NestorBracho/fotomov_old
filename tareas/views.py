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
    if request.method == 'POST':
        formulario = TareaForm(request)
        if formulario.is_valid():
            tarea = Tarea.objects.create(asignado=formulario.cleaned_data['asignado'], nombre=formulario.cleaned_data['nombre'], tarea=formulario.cleaned_data['tarea'], lista=False)
            tarea.save()

    else:
        formulario = TareaForm()
    return render_to_response('tareas/crear_tarea.html', {'formulario': formulario}, context_instance=RequestContext(request))