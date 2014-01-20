from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from clientes.forms import *
from clientes.models import *

def nuevo_macrocliente(request):
    if request.method == 'POST':
        formulario = MacroClienteForm(request.POST)
        if formulario.is_valid():
            print "valido"
            macrocliente = formulario.save()
            print macrocliente.nombre
            return HttpResponseRedirect('/listar_macroclientes/1')
    else:
        formulario = MacroClienteForm()
    return render_to_response('clientes/nuevo_macrocliente.html', {'formulario': formulario}, context_instance = RequestContext(request))

def listar_macrocliente(request, creado):
    macroclientes = MacroCliente.objects.all()
    return render_to_response('clientes/listar_macrocliente.html', {'macroclientes': macroclientes}, context_intance = RequestContext(request))
