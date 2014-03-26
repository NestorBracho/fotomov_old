import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from datetime import *
from django.core import serializers
from administracion.forms import *
from administracion.models import *
from staff.models import *
from productos.models import *
from clientes.models import *
from tareas.models import *
from direcciones.models import *
from direcciones.views import *
import datetime

def nueva_forma_de_pago(request):
    if request.method == 'POST':
        formulario = FormaDePagoForm(request.POST)
        if formulario.is_valid():
            forma_pago = FormaDePago.objects.create(nombre = formulario.cleaned_data['nombre'])
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
    today = datetime.datetime.today()
    #print (today.strftime('%A'))
    #print today
    d = datetime.datetime.today().year
    d= today + datetime.timedelta(days = 1)
    #print (d.strftime('%A'))
    d = (date(1900,4,28).strftime('%A'))
    #print d
    d = date(datetime.datetime.today().year,4,29)
    d = d + datetime.timedelta(days=3, milliseconds=4)
    #print d
    #
    hoy = datetime.datetime.today()
    if request.method == 'POST':
        formulario = GastoForm(request.POST)
        if formulario.is_valid():
            gasto = formulario.save()
            tarea = formulario.cleaned_data['tipo'].nombre+' '+formulario.cleaned_data['nombre']+', '+str(formulario.cleaned_data['monto'])+' en '+formulario.cleaned_data['forma_de_pago'].nombre
            if formulario.cleaned_data['frecuencia'] == 1:
                if formulario.cleaned_data['intervalos_dias'] == 1:
                    dia = "Monday"
                elif formulario.cleaned_data['intervalos_dias'] == 2:
                    dia = "Tuesday"
                elif formulario.cleaned_data['intervalos_dias'] == 3:
                    dia = "Wednesday"
                elif formulario.cleaned_data['intervalos_dias'] == 4:
                    dia = "Thursday"
                elif formulario.cleaned_data['intervalos_dias'] == 5:
                    dia = "Friday"
                elif formulario.cleaned_data['intervalos_dias'] == 6:
                    dia = "Saturday"
                elif formulario.cleaned_data['intervalos_dias'] == 7:
                    dia = "Sunday"
                while (hoy.strftime('%A')) != dia:
                    hoy = hoy + datetime.timedelta(days = 1)
                fech_act = hoy - datetime.timedelta(days = 1)
                Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = formulario.cleaned_data['nombre'], tarea = tarea, es_periodica = True, original = gasto.id, fecha = hoy, fecha_activacion = fech_act)
            elif formulario.cleaned_data['frecuencia'] == 2:
                if hoy.day <= formulario.cleaned_data['intervalos_dias']:
                    hoy = date(hoy.year,hoy.month,formulario.cleaned_data['intervalos_dias'])
                    fech_act = hoy - datetime.timedelta(days = 1)
                    Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = formulario.cleaned_data['nombre'], tarea = tarea, es_periodica = True, original = gasto.id, fecha = hoy, fecha_activacion = fech_act)
                else:
                    dtarea = date(hoy.year,hoy.month,formulario.cleaned_data['intervalos_dias'])
                    dtarea = dtarea + datetime.timedelta(days = 15)
                    if hoy.day <= dtarea.day:
                        if formulario.cleaned_data['intervalos_dias'] == 30:
                            dtarea = date(hoy.year,(hoy.month+1),1)
                            dtarea = dtarea - datetime.timedelta(days = 1)
                            fech_act = dtarea - datetime.timedelta(days = 1)
                            Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = formulario.cleaned_data['nombre'], tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act)
                        else:
                            fech_act = dtarea - datetime.timedelta(days = 1)
                            Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = formulario.cleaned_data['nombre'], tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act)
                    else:
                        dtarea = date(hoy.year,hoy.month,formulario.cleaned_data['intervalos_dias'])
                        aux = dtarea.day
                        dtarea = dtarea + datetime.timedelta(days = 31)
                        dtarea = date(dtarea.year,dtarea.month, aux)
                        fech_act = dtarea - datetime.timedelta(days = 1)
                        Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = formulario.cleaned_data['nombre'], tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act)
            elif formulario.cleaned_data['frecuencia'] == 3:
                if formulario.cleaned_data['intervalos_dias'] == 31:
                    dtarea = date(hoy.year,(hoy.month+1),1)
                    dtarea = dtarea - datetime.timedelta(days = 1)
                    fech_act = dtarea - datetime.timedelta(days = 1)
                    Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = formulario.cleaned_data['nombre'], tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act)
                else:
                    dtarea = date(hoy.year,hoy.month,formulario.cleaned_data['intervalos_dias'])
                    fech_act = dtarea - datetime.timedelta(days = 1)
                    Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = formulario.cleaned_data['nombre'], tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act)
    else:
        formulario = GastoForm()
    return render_to_response('administracion/nuevo_gasto.html', {'formulario': formulario}, context_instance = RequestContext(request))
