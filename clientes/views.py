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

def listar_macroclientes(request, creado):
    macroclientes = MacroCliente.objects.all()
    return render_to_response('clientes/listar_macroclientes.html', {'macroclientes': macroclientes, 'cread0': creado}, context_instance = RequestContext(request))

def editar_macrocliente(request, id_macrocliente):
    if MacroCliente.objects.filter(id = id_macrocliente):
        macrocliente = MacroCliente.objects.get(id = id_macrocliente)
    else:
        return HttpResponseRedirect('/listar_macroclientes/0')
    if request.method == 'POST':
        formulario = MacroClienteForm(request.POST)
        if formulario.is_valid():
            editado = formulario.save(commit=False)
            macrocliente.nombre = editado.nombre
            macrocliente.descripcion = editado.descripcion
            macrocliente.direccion_fiscal = editado.direccion_fiscal
            macrocliente.rif = editado.rif
            macrocliente.submarca = editado.submarca
            macrocliente.telefono = editado.telefono
            macrocliente.save()
            return HttpResponseRedirect('/listar_macroclientes/2')
    else:
        formulario = MacroClienteForm(initial={'submarca': macrocliente.submarca, 'nombre': macrocliente.nombre, 'telefono': macrocliente.telefono, 'rif': macrocliente.rif, 'direccion_fiscal': macrocliente.direccion_fiscal, 'descripcion': macrocliente.descripcion})
    return render_to_response('clientes/nuevo_macrocliente.html', {'formulario': formulario}, context_instance = RequestContext(request))

def ver_macrocliente(request, id_macrocliente):
    if MacroCliente.objects.filter(id = id_macrocliente):
        macrocliente = MacroCliente.objects.get(id = id_macrocliente)
    else:
        return HttpResponseRedirect('/listar_macroclientes/0')
    return render_to_response('clientes/ver_macrocliente.html', {'macrocliente': macrocliente}, context_instance = RequestContext(request))