import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from administracion.forms import *
from administracion.models import *
from staff.models import *
from productos.models import *
from clientes.models import *
from direcciones.models import *
from direcciones.views import *
import datetime

def nueva_forma_de_pago(request):
    if request.method == 'POST':
        formulario = FormaDePagoForm(request.POST)
        if formulario.is_valid():
            forma_pago = TipoDeGasto.objects.create(nombre = formulario.cleaned_data['nombre'])
            forma_pago.save()
    else:
        formulario = FormaDePagoForm()
    return render_to_response('administracion/nueva_forma_de_pago.html', {'formulario': formulario}, context_instance = RequestContext(request))

def nuevo_tipo_de_gasto(request):
    if request.method == 'POST':
        formulario = TipoDeGastoForm(request.POST)
        if formulario.is_valid():
            tipo_gasto = TipoDeGasto.objects.create(nombre = formulario.cleaned_data['nombre'])
            tipo_gasto.save()
    else:
        formulario = TipoDeGastoForm()
    return render_to_response('administracion/nuevo_tipo_de_gasto.html', {'formulario': formulario}, context_instance = RequestContext(request))

def nuevo_gasto(request):
    if request.method == 'POST':
        formulario = GastoForm(request.POST)
    else:
        formulario = GastoForm()
    return render_to_response('administracion/nuevo_gasto.html', {'formulario': formulario}, context_instance = RequestContext(request))
