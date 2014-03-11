import json
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
from staff.models import *
from productos.models import *
from clientes.models import *
from direcciones.models import *
from direcciones.views import *
import datetime

def nuevo_evento(request):
    gastos_predeterminados = Gasto.objects.filter(predeterminado = True)
    direcciones = obtener_direcciones()
    if request.method == 'POST':
        formulario = EventoForm(request.POST)
        if formulario.is_valid():
            print "es valido"
            dias = request.POST.getlist('dias')
            encargado = Encargado.objects.get(id=request.POST.get('encargado'))
            sede = Sede.objects.get(id=request.POST.get('sede'))
            evento = Evento.objects.create(nombre=formulario.cleaned_data['nombre'], descripcion=formulario.cleaned_data['descripcion'],
                                           porcentaje_institucion=formulario.cleaned_data['porcentaje_institucion'], encargado=encargado,
                                           sede=sede, es_stand=formulario.cleaned_data['es_stand'])
            print dias
            for dia in dias:
                dia_split = dia.split('-')
                dia_id = dia_split[0]
                locaciones = request.POST.getlist("locacion" + "-" + dia_id)
                for locacion in locaciones:
                    locacion_split = locacion.split('-')
                    locacion_id = locacion_split[0]
                    locacion_valor = locacion_split[1]
                    locacion_save = Direccion.objects.get(nombre=locacion_valor)
                    funciones = request.POST.getlist("funcion" + "-" + locacion_id)
                    for funcion in funciones:
                        funcion_split = funcion.split('-')
                        funcion_id = funcion_split[0]
                        funcion_valor = funcion_split[1]
                        dia_final = dia_split[3] + "-" + dia_split[2] + "-" + dia_split[1]
                        calcular_entrega = datetime.datetime(int(dia_split[3]), int(dia_split[2]), int(dia_split[1])) + datetime.timedelta(days=15)
                        entrega_split = str(calcular_entrega.date()).split('-')
                        entrega = entrega_split[2] + "-" + entrega_split[1] + "-" + entrega_split[0]
                        funcion_save = Funcion.objects.create(nombre=funcion_valor, evento=evento, dia=dia_final, horas=0, entrega_fotos=entrega, direccion=locacion_save)
                        funcion_save.save()
            return HttpResponseRedirect("/agregar_staff/" + str(evento.id))
    else:
        formulario = EventoForm()
    return render_to_response('evento/nuevo_evento.html', {'formulario': formulario, 'gastos': gastos_predeterminados, 'direcciones': direcciones}, context_instance = RequestContext(request))

def agregar_staff(request, id_evento):
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    tipos_staff = Privilegios.objects.filter(valor=6)
    if request.method == 'POST':
        for funcion in funciones:
            for staff in tipos_staff:
                print str(funcion.id) + "-" + str(staff.id)
                print request.POST.get(str(funcion.id) + "-" + str(staff.id))
                cantidad = request.POST.get(str(funcion.id) + "-" + str(staff.id))
                agregar = StaffPorFuncion.objects.create(tipo=staff, funcion=funcion, cantidad=cantidad)
                agregar.save()
        return HttpResponseRedirect("/agregar_productos/" + id_evento)
    return render_to_response('evento/agregar_staff.html', {'funciones': funciones, 'evento': evento, 'tipos_staff': tipos_staff}, context_instance= RequestContext(request))


def encargado_ajax(request):
    macroC = MacroCliente.objects.get(id=request.GET['id'])
    contacto = Encargado.objects.filter(macrocliente=macroC)
    data = serializers.serialize('json', contacto, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

def sede_ajax(request):
    macroC = MacroCliente.objects.get(id=request.GET['id'])
    contacto = Sede.objects.filter(macrocliente=macroC)
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
    dominio = serializers.serialize('json', locs, fields =('nombre'))
    return HttpResponse(dominio, mimetype='application/json')

def listar_pedidos_sede(request, id_sede):
    return True

def agregar_productos(request,id_evento):
    productos = Producto.objects.all()
    evento = Evento.objects.get(id=id_evento)
    if request.method == 'POST':
        seleccionados = request.POST.getlist('seleccionados')
        for seleccionado in seleccionados:
            precio = request.POST.get(seleccionado)
            producto = Producto.objects.get(id=seleccionado)
            producto_evento = ProductoEvento.objects.create(evento=evento,producto=producto,precio=float(precio))
        return HttpResponseRedirect('/casilla_administrativa/' + id_evento)
    return render_to_response('evento/agregar_productos.html', {'productos': productos}, context_instance=RequestContext(request))

def casilla_administrativa(request, id_evento):
    return render_to_response('evento/casilla_administrativa.html', {}, context_instance=RequestContext(request))

@login_required(login_url='/')
def calendario_de_eventos(request):
    now = datetime.datetime.now()
    user = request.user
    usuario = Usuario.objects.get(usuario=user)
    funciones = StaffPorFuncion.objects.filter(funcion__dia__gt=now.date(), tipo=usuario.privilegio).order_by('-funcion__dia').distinct()
    for funcion in funciones:
        print funcion.funcion.dia
        print funcion.tipo.nombre
    print usuario.nombre
    return render_to_response('evento/calendario_de_eventos.html', {'funciones': funciones,'user': usuario}, context_instance=RequestContext(request))

def marcar_asistencia(request):
    if(request.GET['accion'] == 'r'):
        asistir_evento_c = AsistenciaStaffFuncion.objects.create(usuario = Usuario.objects.get(id = request.GET['userid']), funcion = Funcion.objects.get(id = request.GET['funcionid']))
    else:
        asistir_evento = AsistenciaStaffFuncion.objects.get(usuario = Usuario.objects.get(id = request.GET['userid']), funcion = Funcion.objects.get(id = request.GET['funcionid']))
        asistir_evento.delete()
    data = json.dumps({'status': "hola"})
    return HttpResponse(data, mimetype='application/json')

def usuario_por_evento(request, id_evento):
    funciones = Funcion.objects.filter( evento = Evento.objects.get(id = id_evento))
    return render_to_response('evento/usuario_por_evento.html', {'id_event': funciones}, context_instance=RequestContext(request))