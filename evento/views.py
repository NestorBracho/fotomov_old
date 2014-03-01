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
            dias = request.POST.getlist('dias')
            encargado = Encargado.objects.get(id=request.POST.get('encargado'))
            evento = Evento.objects.create(nombre=formulario.cleaned_data['nombre'], descripcion=formulario.cleaned_data['descripcion'],
                                           porcentaje_institucion=formulario.cleaned_data['porcentaje_institucion'], encargado=encargado)
            for dia in dias:
                dia_split = dia.split('-')
                dia_id = dia_split[0]
                dia_valor = dia_split[1]
                locaciones = request.POST.getlist("locacion" + "-" + dia_id)
                for locacion in locaciones:
                    locacion_split = locacion.split('-')
                    locacion_id = locacion_split[0]
                    locacion_valor = locacion_split[1]
                    funciones = request.POST.getlist("funcion" + "-" + locacion_id)
                    for funcion in funciones:
                        funcion_split = funcion.split('-')
                        funcion_id = funcion_split[0]
                        funcion_valor = funcion_split[1]
                        #funcion_save = Funcion.objects.create(evento=evento, dia=dia_valor, horas=0, entrega_fotos='12/12/2012', )
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