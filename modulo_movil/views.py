from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from evento.forms import *
from evento.models import *
import csv
import time
import os

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
