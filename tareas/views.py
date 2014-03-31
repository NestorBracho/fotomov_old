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
from clientes.models import *
from datetime import *
import datetime

def crear_tarea(request):
    eventos = Evento.objects.all()
    error_fecha = 0
    if request.method == 'POST':
        formulario = TareaForm(request.POST)
        fecha = request.POST.get('fecha')
        if fecha == "":
            error_fecha = 1
            return render_to_response('tareas/crear_tarea.html', {'formulario': formulario, 'eventos': eventos, 'error_fecha': error_fecha}, context_instance=RequestContext(request))
        if formulario.is_valid():
            fecha_split= fecha.split('-')
            fecha_final= fecha_split[2] + "-" + fecha_split[1] + "-" + fecha_split[0]
            evento = request.POST.get('evento')
            if evento == None:
                tarea = Tarea.objects.create(asignado=formulario.cleaned_data['asignado'], nombre=formulario.cleaned_data['nombre'], tarea=formulario.cleaned_data['tarea'],
                                             lista=False, fecha=fecha_final, activa=True)
            else:
                tarea = Tarea.objects.create(asignado=formulario.cleaned_data['asignado'], nombre=formulario.cleaned_data['nombre'], tarea=formulario.cleaned_data['tarea'],
                                             lista=False, fecha=fecha_final, evento=Evento.objects.get(id=evento), activa=True)

            return HttpResponseRedirect('/listar_tareas/')
    else:
        formulario = TareaForm()
    return render_to_response('tareas/crear_tarea.html', {'formulario': formulario, 'eventos': eventos, 'error_fecha': error_fecha}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_tareas(request):
    tareas = Tarea.objects.filter(asignado = Usuario.objects.get(usuario = request.user).privilegio, activa=True)
    return render_to_response('tareas/listar_tareas.html', {'tareas':tareas}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_todas_tareas(request):
    user = request.user
    print user
    usuario = Usuario.objects.get(usuario=user)
    if usuario.privilegio.valor == 1:
        tareas = Tarea.objects.order_by('-fecha')
    else:
        return HttpResponseRedirect('/')
    print tareas
    return render_to_response('tareas/listar_todas_tareas.html', {'tareas': tareas}, context_instance=RequestContext(request))

def modificar_estado_tarea(request):
    #1 pendient
    #2 listo
    #0 NA
    tarea = Tarea.objects.get(id = request.GET['tarea'])
    if request.GET['estado'] == '2':
        tarea.lista = 'True'
    elif request.GET['estado'] == '1':
        tarea.lista = 'False'
    else:
        if tarea.lista == 'None':
            tarea.lista = 'False'
        else:
            tarea.lista = 'None'
    tarea.save()
    data = json.dumps({'status': tarea.lista})
    return HttpResponse(data, mimetype='application/json')

def ver_tarea(request, id_tarea):
    tarea = Tarea.objects.get(id=id_tarea)
    prela = Prela.objects.filter(prela=tarea)
    es_prelada = Prela.objects.filter(es_prelada=tarea)
    return render_to_response('tareas/ver_tarea.html', {'tarea':tarea, 'prela':prela, 'es_prelada': es_prelada}, context_instance=RequestContext(request))

@login_required(login_url='/')
def crear_notificacion(request):
    user = Usuario.objects.get(usuario = request.user)
    if request.method == 'POST':
        formulario = CrearNotificacionFrom(request.POST)
        if formulario.is_valid():
            noti = formulario.cleaned_data['notificacion']
            mCliente = formulario.cleaned_data['macro_cliente']
            cliente = formulario.cleaned_data['cliente']
            nNoti = Notificacion.objects.create(notificacion = noti, macro_cliente = mCliente, cliente = cliente, usuario_creador = user)
            return render_to_response('tareas/crear_notificacion.html', {'formulario': formulario, 'usuario': user, 'flag': 'true'}, context_instance=RequestContext(request))
    else:
        formulario = CrearNotificacionFrom()
    return render_to_response('tareas/crear_notificacion.html', {'formulario': formulario, 'usuario': user, 'flag': 'false'}, context_instance=RequestContext(request))

def listar_notificaciones(request):
    notificaciones = Notificacion.objects.all()
    return render_to_response('tareas/listar_notificaciones.html', {'notificaciones': notificaciones}, context_instance=RequestContext(request))

def ver_notificacion(request, id_notificacion):
    noti = Notificacion.objects.get(id = id_notificacion)
    noti.fue_revisado = True
    noti.save()
    return render_to_response('tareas/ver_notificacion.html', {'notificacion':noti}, context_instance=RequestContext(request))

def eliminar_notificacion(request, id_notificacion):
    notificaciones = Notificacion.objects.all()
    noti = Notificacion.objects.get(id = id_notificacion)
    noti.delete()
    return render_to_response('tareas/listar_notificaciones.html', {'notificaciones': notificaciones}, context_instance=RequestContext(request))

def notificacion_marcar_como_leida(request):
    noti = Notificacion.objects.get(id = request.GET['id'])
    noti.fue_revisado = True
    noti.save()
    data = json.dumps({'status': "hola"})
    return HttpResponse(data, mimetype='application/json')


def notificacion_marcar_como_no_leida(request, id_notificacion):
    noti = Notificacion.objects.get(id = id_notificacion)
    noti.fue_revisado = False
    noti.save()
    notificaciones = Notificacion.objects.all()
    return render_to_response('tareas/listar_notificaciones.html', {'notificaciones': notificaciones}, context_instance=RequestContext(request))

def generar_recursividad(request):
    hoy = datetime.datetime.today()
    tareasHoy = Tarea.objects.filter(fecha = hoy, es_periodica = True)
    for tarea in tareasHoy:
        hoy = hoy + datetime.timedelta(days = 1)
        gast = GastoAdministracion.objects.get(id = tarea.original)
        tarea = gast.tipo.nombre+' '+gast.nombre+', '+str(gast.monto)+' Bs. en '+gast.forma_de_pago.nombre
        if gast.frecuencia == 1:
            if gast.intervalos_dias == 1:
                dia = "Monday"
            elif gast.intervalos_dias == 2:
                dia = "Tuesday"
            elif gast.intervalos_dias == 3:
                dia = "Wednesday"
            elif gast.intervalos_dias == 4:
                dia = "Thursday"
            elif gast.intervalos_dias == 5:
                dia = "Friday"
            elif gast.intervalos_dias == 6:
                dia = "Saturday"
            elif gast.intervalos_dias == 7:
                dia = "Sunday"
            while (hoy.strftime('%A')) != dia:
                hoy = hoy + datetime.timedelta(days = 1)
            fech_act = hoy - datetime.timedelta(days = 1)
            Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = gast.nombre, tarea = tarea, es_periodica = True, original = gasto.id, fecha = hoy, fecha_activacion = fech_act, lista = 'False', activa = True)
        elif gast.frecuencia == 2:
            if hoy.day <= gast.intervalos_dias:
                hoy = date(hoy.year,hoy.month,gast.intervalos_dias)
                fech_act = hoy - datetime.timedelta(days = 1)
                Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = gast.nombre, tarea = tarea, es_periodica = True, original = gasto.id, fecha = hoy, fecha_activacion = fech_act, lista = 'False', activa = True)
            else:
                dtarea = date(hoy.year,hoy.month,gast.intervalos_dias)
                dtarea = dtarea + datetime.timedelta(days = 15)
                if hoy.day <= dtarea.day:
                    if dtarea.day == 30:
                        dtarea = date(hoy.year,(hoy.month+1),1)
                        dtarea = dtarea - datetime.timedelta(days = 1)
                        fech_act = dtarea - datetime.timedelta(days = 1)
                        Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = gast.nombre, tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act, lista = 'False', activa = True)
                    else:
                        fech_act = dtarea - datetime.timedelta(days = 1)
                        Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = gast.nombre, tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act, lista = 'False', activa = True)
                else:
                    dtarea = date(hoy.year,hoy.month,gast.intervalos_dias)
                    aux = dtarea.day
                    dtarea = dtarea + datetime.timedelta(days = 31)
                    dtarea = date(dtarea.year,dtarea.month, aux)
                    fech_act = dtarea - datetime.timedelta(days = 1)
                    Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = gast.nombre, tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act, lista = 'False', activa = True)
        elif gast.frecuencia == 3:
            if gast.intervalos_dias == 31:
                dtarea = date(hoy.year,(hoy.month+1),1)
                dtarea = dtarea - datetime.timedelta(days = 1)
                fech_act = dtarea - datetime.timedelta(days = 1)
                Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = gast.nombre, tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act, lista = 'False', activa = True)
            else:
                dtarea = date(hoy.year,hoy.month,gast.intervalos_dias)
                fech_act = dtarea - datetime.timedelta(days = 1)
                Tarea.objects.create(asignado = Privilegios.objects.get(valor = 5), nombre = gast.nombre, tarea = tarea, es_periodica = True, original = gasto.id, fecha = dtarea, fecha_activacion = fech_act, lista = 'False', activa = True)
    return HttpResponseRedirect('/escritorio/')