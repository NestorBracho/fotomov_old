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
from tareas.models import *
from modulo_movil.models import *
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
                                           sede=sede, tipo=formulario.cleaned_data['tipo'], macrocliente=formulario.cleaned_data['macrocliente'])
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
                        directorio = direccionFuncion.objects.create(funcion=funcion_save, dir = funcion_save.evento.macrocliente.submarca.marca.nombre + "/" + funcion_save.evento.macrocliente.submarca.nombre + "/" + funcion_save.evento.macrocliente.nombre + "/" + funcion_save.evento.nombre + "/" + funcion_save.dia + "/" + funcion_save.direccion.nombre + "/" +funcion_save.nombre)
            #Empieza a crear las tareas del evento
            tareas = TareaTipoEvento.objects.filter(tipo_evento=evento.tipo)
            fechas = Funcion.objects.filter(evento=evento).order_by('dia')
            for fecha in fechas:
                print fecha.dia
            print "las que saque"
            fecha_ini = fechas[0].dia
            fecha_fin = fechas[len(fechas) - 1].dia
            prueba_antes = fecha_ini - datetime.timedelta(days=2)
            print fecha_ini
            print prueba_antes
            for tarea in tareas:
                if tarea.dias > 0:
                    tarea_evento = Tarea.objects.create(asignado=tarea.asignado, nombre=tarea.nombre, tarea=tarea.tarea, lista="False", evento=evento,
                                                    fecha_activacion= fecha_ini - datetime.timedelta(days=tarea.dias), fecha=fecha_ini, original=tarea.id)
                else:
                    tarea_evento = Tarea.objects.create(asignado=tarea.asignado, nombre=tarea.nombre, tarea=tarea.tarea, lista="False", evento=evento,
                                                        fecha_activacion= fecha_fin + datetime.timedelta(days=(-tarea.dias)), fecha=fecha_ini, original=tarea.id)
            prelaciones = PrelaTareaTipoEvento.objects.filter(tipo_evento=evento.tipo)
            for prelacion in prelaciones:
                es_prelada = Tarea.objects.get(evento=evento, original=prelacion.es_prelada.id)
                prela = Tarea.objects.get(evento=evento, original=prelacion.prela.id)
                prelacion_evento = Prela.objects.create(es_prelada=es_prelada, prela=prela)
                prelacion_evento.save()
            return HttpResponseRedirect("/listar_evento/1")
    else:
        formulario = EventoForm()
    return render_to_response('evento/nuevo_evento.html', {'formulario': formulario, 'gastos': gastos_predeterminados, 'direcciones': direcciones}, context_instance = RequestContext(request))

def agregar_staff(request, id_evento):
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    tipos_staff = Privilegios.objects.filter(valor=6)
    lista = []
    for funcion in funciones:
        staff = StaffPorFuncion.objects.filter(funcion=funcion)
        if staff:
            tupla = (funcion,staff)
            lista.append(tupla)
        else:
            for tipo in tipos_staff:
                creado = StaffPorFuncion.objects.create(tipo=tipo, funcion=funcion, cantidad=0)
            staff = StaffPorFuncion.objects.filter(funcion=funcion)
            if staff:
                tupla = (funcion,staff)
                lista.append(tupla)
    if request.method == 'POST':
        for funcion in funciones:
            for staff in tipos_staff:
                print str(funcion.id) + "-" + str(staff.id)
                print request.POST.get(str(funcion.id) + "-" + str(staff.id))
                cantidad = request.POST.get(str(funcion.id) + "-" + str(staff.id))
                agregar = StaffPorFuncion.objects.create(tipo=staff, funcion=funcion, cantidad=cantidad)
                agregar.save()
        return HttpResponseRedirect("/listar_evento/2")
    print lista
    return render_to_response('evento/agregar_staff.html', {'funciones': lista, 'evento': evento}, context_instance= RequestContext(request))


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

def listar_evento(request, creado):
    eventos = Evento.objects.all()
    return render_to_response('evento/listar_evento.html', {'eventos':eventos, 'creado': creado}, context_instance = RequestContext(request))

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
    lista = []
    for producto in productos:
        if ProductoEvento.objects.filter(evento=evento, producto=producto):
            producto_existente = ProductoEvento.objects.get(evento=evento, producto=producto)
            print producto_existente.precio
            tupla=(producto,1, producto_existente.precio)
            print tupla[2]
        else:
            tupla = (producto,0,0)
        lista.append(tupla)

    if request.method == 'POST':
        seleccionados = request.POST.getlist('seleccionados')
        existentes = ProductoEvento.objects.filter(evento=evento)
        for existente in existentes:
            existente.delete()
        for seleccionado in seleccionados:
            precio = request.POST.get(seleccionado)
            producto = Producto.objects.get(id=seleccionado)
            producto_evento = ProductoEvento.objects.create(evento=evento,producto=producto,precio=float(precio.replace(',','.')))
        return HttpResponseRedirect('/listar_evento/2')
    print lista
    return render_to_response('evento/agregar_productos.html', {'productos': lista}, context_instance=RequestContext(request))

def casilla_administrativa(request, id_evento):
    return render_to_response('evento/casilla_administrativa.html', {}, context_instance=RequestContext(request))

@login_required(login_url='/')
def calendario_de_eventos(request):
    now = datetime.datetime.now()
    user = request.user
    usuario = Usuario.objects.get(usuario=user)
    funciones = StaffPorFuncion.objects.filter(funcion__dia__gt=now.date(), tipo=usuario.privilegio, cantidad__gt = 0).order_by('-funcion__dia').distinct()
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
    even = Evento.objects.get(id = id_evento)
    funciones = Funcion.objects.filter( evento = even)
    priv = Privilegios.objects.filter( valor = 6)
    return render_to_response('evento/usuario_por_evento.html', {'funciones': funciones, 'staff':priv, 'evento': even}, context_instance=RequestContext(request))

def get_staff_usuario_por_evento(request):
    elStaff = StaffPorFuncion.objects.filter(funcion = Funcion.objects.get( id = request.GET['funcion']), cantidad__gt = 0)
    data = serializers.serialize('json', elStaff, fields =('tipo','cantidad'))
    return HttpResponse(data, mimetype='application/json')

def get_staff_usuarios_usuario_por_evento(request):
    if(request.GET['marc']=='0'):
        asistencia = AsistenciaStaffFuncion.objects.filter(usuario__privilegio = Privilegios.objects.get( id = request.GET['staff']), funcion = Funcion.objects.get(id = request.GET['funcion']))
        aux = []
        gente = []
        for asistente in asistencia:
            tupla = (asistente.usuario, asistente.fue_convocado)
            aux.append(asistente.fue_convocado)
            gente.append(asistente.usuario)
            print gente
        data = serializers.serialize('json', gente, fields =('nombre','apellido','email','equipos','telefono_celular'))
    else:
        tipo = AsistenciaStaffFuncion.objects.filter( usuario = Usuario.objects.get(id = request.GET['usuario']), funcion = Funcion.objects.get(id = request.GET['funcion']))
        data = serializers.serialize('json', tipo, fields =('fue_convocado'))
    return HttpResponse(data, mimetype='application/json')

def convocar_usuario_a_evento(request):
    staff = AsistenciaStaffFuncion.objects.get(usuario = Usuario.objects.get(id = request.GET['usuario']), funcion = Funcion.objects.get(id = request.GET['funcion']))
    if (staff.fue_convocado == False):
        staff.fue_convocado = True
        staff.save()
    else:
        staff.fue_convocado = False
        staff.save()
    data = json.dumps({'status': "hola"})
    return HttpResponse(data, mimetype='application/json')

def nuevo_tipo_de_evento(request, creado):
    tipo_eventos = Tipos_Eventos.objects.all()
    staff = Privilegios.objects.filter(valor__lt = 6)
    prelaciones = []
    if(request.method == 'POST'):
        formulario = TiposEventoForm(request.POST)
        if(formulario.is_valid()):
            tipoE = formulario.save()
            tareas = int(request.POST['tareas'])
            for tarea in range(1, tareas+1):
                nom = request.POST['nom-'+str(tarea)]
                desc = request.POST['desc-'+str(tarea)]
                staffneed = request.POST['select-staff-'+str(tarea)]
                dias = request.POST['dias-'+str(tarea)]
                aod = request.POST['aod-'+str(tarea)]
                prel = request.POST['prel-'+str(tarea)]
                if aod == 'False':
                    dias = int(dias)*(-1)
                print staffneed
                TTE = TareaTipoEvento.objects.create(asignado = Privilegios.objects.get(id = staffneed), nombre = nom, tarea = desc, tipo_evento = tipoE, dias = dias, id_aux = str(tarea))
                if prel != '0':
                    aux = str(tarea)+"-"+request.POST['prel-'+str(tarea)]
                    prelaciones.append(aux)
            for prelacion in prelaciones:
                aux = prelacion.split('-')
                tarea1 = TareaTipoEvento.objects.get(tipo_evento = tipoE, id_aux = aux[1])
                tarea2 = TareaTipoEvento.objects.get(tipo_evento = tipoE, id_aux = aux[0])
                PrelaTareaTipoEvento.objects.create(es_prelada = tarea1, prela = tarea2, tipo_evento=tipoE)
            for tarea in range(1, tareas+1):
                TareaAux = TareaTipoEvento.objects.get(tipo_evento = tipoE, id_aux = str(tarea))
                TareaAux.id_aux = None
                TareaAux.save()
            return render_to_response('evento/nuevo_tipo_de_evento.html', {'formulario': formulario, 'eventos':tipo_eventos, 'staff':staff, 'creado':creado}, context_instance=RequestContext(request))
    else:
        formulario = TiposEventoForm()
    return render_to_response('evento/nuevo_tipo_de_evento.html', {'formulario': formulario, 'eventos':tipo_eventos, 'staff':staff, 'creado':creado}, context_instance=RequestContext(request))

def nueva_pauta(request, id_evento):
    evento = Evento.objects.get(id=id_evento)
    if request.method == 'POST':
        formulario = PautaForm(request.POST)
        if formulario.is_valid():
            pauta = formulario.cleaned_data['pauta']
            nombre = formulario.cleaned_data['nombre']
            nueva_pauta = Pautas.objects.create(nombre=nombre, pauta=pauta, evento=evento)
            nueva_pauta.save()
            return HttpResponseRedirect('/listar_pautas/' + str(evento.id) + '/1')
    else:
        formulario = PautaForm()
    return render_to_response('evento/nueva_pauta.html', {'formulario': formulario, 'evento': evento}, context_instance=RequestContext(request))

def listar_pautas(request, id_evento, creado):
    evento = Evento.objects.get(id=id_evento)
    pautas = Pautas.objects.filter(evento=evento)
    return render_to_response('evento/listar_pautas.html', {'pautas': pautas, 'evento': evento, 'creado': creado}, context_instance=RequestContext(request))

def editar_pauta(request, id_pauta):
    pauta = Pautas.objects.get(id=id_pauta)
    if request.method == 'POST':
        formulario = PautaForm(request.POST)
        if formulario.is_valid():
            pauta.nombre = formulario.cleaned_data['nombre']
            pauta.pauta = formulario.cleaned_data['pauta']
            pauta.save()
            return HttpResponseRedirect('/listar_pautas/' + str(pauta.evento.id) + '/2')
    else:
        formulario = PautaForm(initial={'nombre': pauta.nombre, 'pauta': pauta.pauta})
    return render_to_response('evento/nueva_pauta.html', {'formulario': formulario}, context_instance=RequestContext(request))

def eliminar_pauta(request, id_pauta):
    pauta = Pautas.objects.get(id=id_pauta)
    id_evento = pauta.evento.id
    pauta.delete()
    return HttpResponseRedirect("/listar_pautas/" + str(id_evento) + "/3")

def ver_pauta(request, id_pauta):
    pauta = Pautas.objects.get(id=id_pauta)
    return render_to_response('evento/ver_pauta.html', {'pauta': pauta}, context_instance=RequestContext(request))