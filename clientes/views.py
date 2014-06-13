import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import simplejson
from clientes.forms import *
from clientes.models import *
from productos.forms import *
from productos.models import *
from staff.models import Privilegios, StaffPorFuncion
from marca.forms import *
from marca.models import *
from evento.models import *
from tareas.models import Notificacion
from direcciones.models import *
from direcciones.views import *
import datetime

@login_required(login_url='/')
def nuevo_macrocliente(request):
    direcciones = obtener_direcciones()
    if request.method == 'POST':
        formularioM = MacroClienteForm(request.POST)
        formularioR = MacroClienteContactoForm(request.POST)
        if formularioM.is_valid() and formularioR.is_valid():
            subMacrocliente = formularioM.cleaned_data['submarca']
            nomMacrocliente = formularioM.cleaned_data['nombre']
            telMacrocliente = formularioM.cleaned_data['telefono']
            rifMacrocliente = formularioM.cleaned_data['rif']
            dfMacrocliente = formularioM.cleaned_data['direccion_fiscal']
            descMacrocliente = formularioM.cleaned_data['descripcion']
            contacNombre = formularioR.cleaned_data['nombreContacto']
            contacCedula = formularioR.cleaned_data['cedula']
            contacTelefono = formularioR.cleaned_data['telefono']
            contacDescripcion = formularioR.cleaned_data['descripcion_contacto']
            contactoEmail = formularioR.cleaned_data['email']
            contactoCargo = formularioR.cleaned_data['cargo']
            macrocliente = MacroCliente.objects.create(submarca=subMacrocliente, nombre=nomMacrocliente, telefono=telMacrocliente, rif=rifMacrocliente, direccion_fiscal=dfMacrocliente, descripcion=descMacrocliente)
            encargado = Encargado.objects.create(macrocliente=macrocliente, cargo=contactoCargo, nombre=contacNombre, cedula=contacCedula, telefono=contacTelefono, descripcion=contacDescripcion, email=contactoEmail)
            direcciones = request.POST.getlist('sedes')
            for direccion in direcciones:
                dir = Direccion.objects.get(nombre=direccion)
                nombre = request.POST.get(direccion)
                sede = Sede.objects.create(macrocliente=macrocliente, direccion=dir, nombre=nombre)
                sede.save()
            macrocliente.save()
            encargado.save()
            print macrocliente.nombre
            return HttpResponseRedirect('/listar_macroclientes/1')
    else:
        formularioM = MacroClienteForm()
        formularioR = MacroClienteContactoForm()
    return render_to_response('clientes/nuevo_macrocliente.html', {'formularioM': formularioM, 'formularioR': formularioR, 'direcciones': direcciones}, context_instance = RequestContext(request))

@login_required(login_url='/')
def listar_macroclientes(request, creado):
    macroclientes = MacroCliente.objects.all().exclude(id=1)
    return render_to_response('clientes/listar_macroclientes.html', {'macroclientes': macroclientes, 'creado': creado}, context_instance = RequestContext(request))

@login_required(login_url='/')
def editar_macrocliente(request, id_macrocliente):
    direccionesL = obtener_direcciones()
    if MacroCliente.objects.filter(id = id_macrocliente):
        macrocliente = MacroCliente.objects.get(id = id_macrocliente)

    else:
        return HttpResponseRedirect('/listar_macroclientes/0')
    dirs = Sede.objects.filter(macrocliente=macrocliente)
    submarcas = SubMarca.objects.filter(marca=macrocliente.submarca.marca)
    for submarca in submarcas:
        print submarca.nombre
    if request.method == 'POST':
        macrocliente.rif = "nulo"
        formulario = MacroClienteForm(request.POST)
        print macrocliente.rif
        macrocliente.save()
        if formulario.is_valid():
            print "entro"
            editado = formulario.save(commit=False)
            macrocliente.nombre = editado.nombre
            macrocliente.descripcion = editado.descripcion
            macrocliente.direccion_fiscal = editado.direccion_fiscal
            macrocliente.rif = editado.rif
            macrocliente.submarca = editado.submarca
            macrocliente.telefono = editado.telefono
            macrocliente.save()
            for dir in dirs:
                dir.delete()
            direcciones = request.POST.getlist('sedes')
            direcciones = request.POST.getlist('sedes')
            for direccion in direcciones:
                dir = Direccion.objects.get(nombre=direccion)
                nombre = request.POST.get(direccion)
                sede = Sede.objects.create(macrocliente=macrocliente, direccion=dir, nombre=nombre)
                sede.save()
            return HttpResponseRedirect('/listar_macroclientes/2')
    else:
        formulario = MacroClienteForm(initial={'marca': macrocliente.submarca.marca, 'nombre': macrocliente.nombre, 'telefono': macrocliente.telefono, 'rif': macrocliente.rif, 'direccion_fiscal': macrocliente.direccion_fiscal, 'descripcion': macrocliente.descripcion})
    return render_to_response('clientes/editar_macrocliente.html', {'submarcas': submarcas, 'formulario': formulario, 'dirs': dirs, 'macrocliente': macrocliente, 'direcciones': direccionesL}, context_instance = RequestContext(request))

@login_required(login_url='/')
def ver_macrocliente(request, id_macrocliente):
    if MacroCliente.objects.filter(id = id_macrocliente):
        macrocliente = MacroCliente.objects.get(id = id_macrocliente)
        sedes = Sede.objects.filter(macrocliente=macrocliente)
        print sedes
        if len(sedes) > 0:
            tienedir = True
            primeraDir = sedes[0]
        else:
            tienedir = False
            primeraDir = None
    else:
        return HttpResponseRedirect('/listar_macroclientes/0')
    return render_to_response('clientes/ver_macrocliente.html', {'macrocliente': macrocliente, 'tienedir': tienedir, 'primeraDir': primeraDir, 'sedes': sedes}, context_instance = RequestContext(request))

@login_required(login_url='/')
def eliminar_macrocliente(request, id_macrocliente):
    if MacroCliente.objects.filter(id=id_macrocliente):
        MacroCliente.objects.get(id=id_macrocliente).delete()
        pass
    else:
        return HttpResponseRedirect('/listar_macroclientes/4')
    return HttpResponseRedirect('/listar_macroclientes/3')

@login_required(login_url='/')
def listar_contactos_macrocliente(request, id_macrocliente, creado):
    if MacroCliente.objects.filter(id=id_macrocliente):
        macrocliente = MacroCliente.objects.get(id=id_macrocliente)
        contactos = Encargado.objects.filter(macrocliente=macrocliente)
    else:
        return HttpResponseRedirect('/listar_macroclientes/4')
    return render_to_response('clientes/listar_contactos_macrocliente.html', {'contactos': contactos, 'macrocliente': macrocliente, 'creado': creado}, context_instance = RequestContext(request))

@login_required(login_url='/')
def nuevo_contacto_macrocliente(request, id_macrocliente):
    if MacroCliente.objects.filter(id=id_macrocliente):
        macrocliente = MacroCliente.objects.get(id=id_macrocliente)
    else:
        return HttpResponseRedirect('/listar_macroclientes/4')
    if request.method == 'POST':
        formulario = MacroClienteContactoForm(request.POST)
        if formulario.is_valid():
            nombreContacto = formulario.cleaned_data['nombreContacto']
            cedula = formulario.cleaned_data['cedula']
            cargo = formulario.cleaned_data['cargo']
            telefono = formulario.cleaned_data['telefono']
            email = formulario.cleaned_data['email']
            descripcion = formulario.cleaned_data['descripcion_contacto']
            encargado = Encargado.objects.create(macrocliente=macrocliente, nombre=nombreContacto, cedula=cedula, cargo=cargo, telefono=telefono, email=email, descripcion=descripcion)
            return HttpResponseRedirect('/listar_contactos_macrocliente/' + str(macrocliente.id) + '/1')
        else:
            print "no entro"
    else:
        formulario = MacroClienteContactoForm()
    return render_to_response('clientes/nuevo_contacto_macrocliente.html', {'formulario': formulario, 'nuevo': True}, context_instance = RequestContext(request))

@login_required(login_url='/')
def editar_contacto_macrocliente(request, id_contacto):
    if Encargado.objects.filter(id=id_contacto):
        contacto = Encargado.objects.get(id=id_contacto)
        macrocliente = MacroCliente.objects.get(id=contacto.macrocliente.id)
    else:
        return HttpResponseRedirect('/listar_contactos_macrocliente/' + str(macrocliente.id) + '/4')
    if request.method == 'POST':
        formulario = MacroClienteContactoForm(request.POST)
        if formulario.is_valid():
            form = formulario.save(commit=False)
            contacto.macrocliente = macrocliente
            contacto.cedula = form.cedula
            contacto.descripcion = form.descripcion
            contacto.email = form.email
            contacto.nombre = form.nombre
            contacto.telefono = form.telefono
            contacto.save()
            print macrocliente.id
            return HttpResponseRedirect('/listar_contactos_macrocliente/' + str(macrocliente.id) + '/2')
    else:
        formulario = MacroClienteContactoForm(initial={'nombreContacto': contacto.nombre, 'cedula': contacto.cedula, 'telefono': contacto.telefono, 'email': contacto.email, 'descripcion_contacto': contacto.descripcion})
    return render_to_response('clientes/nuevo_contacto_macrocliente.html', {'formulario': formulario, 'nuevo': False}, context_instance = RequestContext(request))

@login_required(login_url='/')
def eliminar_contacto_macrocliente(request, id_contacto):
    if Encargado.objects.filter(id=id_contacto):
        encargado = Encargado.objects.get(id=id_contacto)
        macrocliente = encargado.macrocliente
        encargado.delete()
    else:
        return HttpResponseRedirect('/listar_contactos_macrocliente/' + str(macrocliente.id) + '/4')
    return HttpResponseRedirect('/listar_contactos_macrocliente/' + str(macrocliente.id) + '/3')

@login_required(login_url='/')
def ver_contacto_macrocliente(request, id_contacto):
    contacto = Encargado.objects.get(id=id_contacto)
    return render_to_response('clientes/ver_contacto_macrocliente.html', {'contacto': contacto}, context_instance = RequestContext(request))

def nuevo_macrocliente_ajax(request):
    marca = Marca.objects.get(id = request.GET['id'])
    submarcas = SubMarca.objects.filter(marca = marca)
    data = serializers.serialize('json', submarcas, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def nuevo_cliente(request):
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            cliente = formulario.save()
            return HttpResponseRedirect('/listar_clientes/1')
    else:
        formulario = ClienteForm()
    return render_to_response('clientes/nuevo_cliente.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_clientes(request, creado):
    clientes = Cliente.objects.filter()
    return render_to_response('clientes/listar_cliente.html', {'clientes': clientes, 'creado': creado}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_cliente(request, id_cliente):
    cliente = Cliente.objects.get(id=id_cliente)
    clienteF = ClienteForm()
    pedidos = Pedido.objects.filter(cliente=id_cliente)
    eventos = Evento.objects.filter(cliente=cliente)
    notificaciones = Notificacion.objects.filter(cliente=cliente)
    return render_to_response('clientes/ver_cliente.html', {'cliente': cliente, 'pedidos':pedidos,
                                                            'clienteForm':clienteF, 'eventos': eventos,
                                                            'notificaciones': notificaciones}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_cliente(request, id_cliente):
    cliente = Cliente.objects.get(id=id_cliente)
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            newcliente = formulario.save(commit=False)
            cliente.nombres = newcliente.nombres
            cliente.apellidos = newcliente.apellidos
            cliente.telefono = newcliente.telefono
            cliente.email = newcliente.email
            cliente.direccion_fiscal = newcliente.direccion_fiscal
            cliente.rif = newcliente.rif
            cliente.cedula = newcliente.cedula
            cliente.save()
            return HttpResponseRedirect('/listar_clientes')
    else:
        formulario = ClienteForm(initial={'nombres': cliente.nombres, 'apellidos': cliente.apellidos, 'telefono': cliente.telefono, 'email': cliente.email,
                                 'direccion_fiscal': cliente.direccion_fiscal, 'rif': cliente.rif, 'cedula': cliente.cedula})
    return render_to_response('clientes/nuevo_cliente.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_cliente(request, id_cliente):
    cliente = Cliente.objects.get(id=id_cliente).delete()
    return HttpResponseRedirect('/listar_clientes')

def agregar_sede_macrocliente_ajax(request):
    if Direccion.objects.filter(nombre = request.GET['direc']).count() == 0:
        dirc = 0
    else:
        dirc = 1
    data = json.dumps({'status': dirc})
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def listar_eventos_macrocliente(request, id_macrocliente):
    macrocliente = MacroCliente.objects.get(id=id_macrocliente)
    eventos = Evento.objects.filter(macrocliente__id=id_macrocliente)
    return render_to_response('evento/listar_evento.html', {'eventos': eventos, 'macrocliente': macrocliente}, context_instance = RequestContext(request))


def traer_cliente_evento(request):
    usuarioN = Cliente.objects.filter(nombres__contains = request.GET['usu'])
    usuarioA = Cliente.objects.filter(apellidos__contains = request.GET['usu'])
    usuarioC = Cliente.objects.filter(cedula__contains = request.GET['usu'])

    aux = []

    for usuario in usuarioN:
        flag = False
        for au in aux:
            if au == usuario:
                flag = True
        if flag == False:
            aux.append(usuario)

    for usuario in usuarioA:
        flag = False
        for au in aux:
            if au == usuario:
                flag = True
        if flag == False:
            aux.append(usuario)

    for usuario in usuarioC:
        flag = False
        for au in aux:
            if au == usuario:
                flag = True
        if flag == False:
            aux.append(usuario)

    usuarioN = aux
    resp = []

    for usuario in usuarioN:
        resp.append({"value": usuario.id, "label": usuario.nombres+" "+usuario.apellidos, "desc": usuario.cedula})

    print resp

    return HttpResponse(simplejson.dumps(resp), mimetype='application/json')
