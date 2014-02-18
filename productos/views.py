from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from productos.models import *
from productos.forms import *

def nuevo_producto(request):
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()

    else:
        formulario = ProductoForm()
    return render_to_response('productos/nuevo_producto.html', {'formulario': formulario}, context_instance=RequestContext(request))

def editar_producto(request):
    if request.method == 'POST':
        pass
    else:
        pass
    return render_to_response('productos/nuevo_producto.html', {}, context_instance=RequestContext(request))

def eliminar_producto(request):
    return True