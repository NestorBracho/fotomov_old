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
from clientes.models import *
from direcciones.models import *

def nuevo_evento(request):
    gastos_predeterminados = Gasto.objects.filter(predeterminado = True)
    if request.method == 'POST':
        formulario = EventoForm(request.POST)
        if formulario.is_valid():
            print "funcion"
    else:
        formulario = EventoForm()
    return render_to_response('evento/nuevo_evento.html', {'formulario': formulario, 'gastos': gastos_predeterminados}, context_instance = RequestContext(request))

def encargado_ajax(request):
    macroC = MacroCliente.objects.get(id=request.GET['id'])
    contacto = Encargado.objects.filter(macrocliente=macroC)
    data = serializers.serialize('json', contacto, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

def listar_evento(request):
    eventos = Evento.objects.all()
    return render_to_response('evento/listar_evento.html', {'eventos':eventos}, context_instance = RequestContext(request))

def locacion_ajax(request):
    locaciones = Direccion.objects.filter(nombre__contains=request.GET['locacion'])
    if len(locaciones)>0:
        i=0
        locs=[]
        while i < 5 and i<len(locaciones):
            locs.append(locaciones[i])
            i = i+1
    else:
        locs = None
    data = serializers.serialize('json', locs, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

def listar_pedidos_sede(request, id_sede):
    return True