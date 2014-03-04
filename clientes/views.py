import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from clientes.forms import *
from clientes.models import *
from marca.forms import *
from marca.models import *
from direcciones.models import *

def nuevo_macrocliente(request):
    if request.method == 'POST':
        formularioM = MacroClienteForm(request.POST)
        formularioR = MacroClienteContactoForm(request.POST)
        print "antes del valid"
        if formularioM.is_valid() and formularioR.is_valid():
            print "entro"
            subMacrocliente = formularioM.cleaned_data['submarca']
            nomMacrocliente = formularioM.cleaned_data['nombre']
            telMacrocliente = formularioM.cleaned_data['telefono']
            rifMacrocliente = formularioM.cleaned_data['rif']
            dfMacrocliente = formularioM.cleaned_data['direccion_fiscal']
            descMacrocliente = formularioM.cleaned_data['descripcion']
            contacNombre = formularioR.cleaned_data['nombreContacto']
            contacCedula = formularioR.cleaned_data['cedula']
            contacTelefono = formularioR.cleaned_data['telefono']
            contacDescripcion = formularioR.cleaned_data['descripcion']
            contactoEmail = formularioR.cleaned_data['email']
            contactoCargo = formularioR.cleaned_data['cargo']
            macrocliente = MacroCliente.objects.create(submarca=subMacrocliente, nombre=nomMacrocliente, telefono=telMacrocliente, rif=rifMacrocliente, direccion_fiscal=dfMacrocliente, descripcion=descMacrocliente)
            macrocliente.save()
            encargado = Encargado.objects.create(macrocliente=macrocliente, cargo=contactoCargo, nombre=contacNombre, cedula=contacCedula, telefono=contacTelefono, descripcion=contacDescripcion, email=contactoEmail)
            encargado.save()
            direcciones = request.POST.getlist('dir')
            i = 0
            while i < len(direcciones):
                direccion = Direccion.objects.create(macrocliente=macrocliente, direccion=direcciones[i], lat=direcciones[i+2], lon=direcciones[i+3], descripcion=direcciones[i+1])
                direccion.save()
                i += 4
            print macrocliente.nombre
            return HttpResponseRedirect('/listar_macroclientes/1')
    else:
        formularioM = MacroClienteForm()
        formularioR = MacroClienteContactoForm()
    return render_to_response('clientes/nuevo_macrocliente.html', {'formularioM': formularioM, 'formularioR': formularioR}, context_instance = RequestContext(request))

def listar_macroclientes(request, creado):
    macroclientes = MacroCliente.objects.all()
    return render_to_response('clientes/listar_macroclientes.html', {'macroclientes': macroclientes, 'creado': creado}, context_instance = RequestContext(request))

def editar_macrocliente(request, id_macrocliente):
    if MacroCliente.objects.filter(id = id_macrocliente):
        macrocliente = MacroCliente.objects.get(id = id_macrocliente)
    else:
        return HttpResponseRedirect('/listar_macroclientes/0')
    dirs = Direccion.objects.filter(macrocliente=macrocliente)
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
            for dir in dirs:
                dir.delete()
            direcciones = request.POST.getlist('dir')
            i = 0
            while i < len(direcciones):
                direccion = Direccion.objects.create(macrocliente=macrocliente, direccion=direcciones[i], lat=direcciones[i+2], lon=direcciones[i+3], descripcion=direcciones[i+1])
                direccion.save()
                i += 4
            return HttpResponseRedirect('/listar_macroclientes/2')
    else:
        formulario = MacroClienteForm(initial={'submarca': macrocliente.submarca, 'nombre': macrocliente.nombre, 'telefono': macrocliente.telefono, 'rif': macrocliente.rif, 'direccion_fiscal': macrocliente.direccion_fiscal, 'descripcion': macrocliente.descripcion})
    return render_to_response('clientes/editar_macrocliente.html', {'formulario': formulario, 'direcciones': dirs}, context_instance = RequestContext(request))

def ver_macrocliente(request, id_macrocliente):
    if MacroCliente.objects.filter(id = id_macrocliente):
        macrocliente = MacroCliente.objects.get(id = id_macrocliente)
        sedes = Sede.objects.filter(id=id_macrocliente)
        if len(sedes) > 0:
            tienedir = True
            primeraDir = sedes[0]
        else:
            tienedir = False
            primeraDir = None
    else:
        return HttpResponseRedirect('/listar_macroclientes/0')
    return render_to_response('clientes/ver_macrocliente.html', {'macrocliente': macrocliente, 'tienedir': tienedir, 'primeraDir': primeraDir, 'sedes': sedes}, context_instance = RequestContext(request))

def eliminar_macrocliente(request, id_macrocliente):
    if MacroCliente.objects.filter(id=id_macrocliente):
        MacroCliente.objects.get(id=id_macrocliente).delete()
        pass
    else:
        return HttpResponseRedirect('/listar_macroclientes/4')
    return HttpResponseRedirect('/listar_macroclientes/3')

def listar_contactos_macrocliente(request, id_macrocliente, creado):
    if MacroCliente.objects.filter(id=id_macrocliente):
        macrocliente = MacroCliente.objects.get(id=id_macrocliente)
        contactos = Encargado.objects.filter(macrocliente=macrocliente)
    else:
        return HttpResponseRedirect('/listar_macroclientes/4')
    return render_to_response('clientes/listar_contactos_macrocliente.html', {'contactos': contactos, 'macrocliente': macrocliente, 'creado': creado}, context_instance = RequestContext(request))

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
            descripcion = formulario.cleaned_data['descripcion']
            encargado = Encargado.objects.create(macrocliente=macrocliente, nombre=nombreContacto, cedula=cedula, cargo=cargo, telefono=telefono, email=email, descripcion=descripcion)
            return HttpResponseRedirect('/listar_contactos_macrocliente/' + str(macrocliente.id) + '/1')
        else:
            print "no entro"
    else:
        formulario = MacroClienteContactoForm()
    return render_to_response('clientes/nuevo_contacto_macrocliente.html', {'formulario': formulario, 'nuevo': True}, context_instance = RequestContext(request))

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
        formulario = MacroClienteContactoForm(initial={'nombre': contacto.nombre, 'cedula': contacto.cedula, 'telefono': contacto.telefono, 'email': contacto.email, 'descripcion': contacto.descripcion})
    return render_to_response('clientes/nuevo_contacto_macrocliente.html', {'formulario': formulario, 'nuevo': False}, context_instance = RequestContext(request))

def eliminar_contacto_macrocliente(request, id_contacto):
    if Encargado.objects.filter(id=id_contacto):
        encargado = Encargado.objects.get(id=id_contacto)
        macrocliente = encargado.macrocliente
        encargado.delete()
    else:
        return HttpResponseRedirect('/listar_contactos_macrocliente/' + str(macrocliente.id) + '/4')
    return HttpResponseRedirect('/listar_contactos_macrocliente/' + str(macrocliente.id) + '/3')

def ver_contacto_macrocliente(request, id_contacto):
    contacto = Encargado.objects.get(id=id_contacto)
    return render_to_response('clientes/ver_contacto_macrocliente.html', {'contacto': contacto}, context_instance = RequestContext(request))

def nuevo_macrocliente_ajax(request):
    marca = Marca.objects.get(id = request.GET['id'])
    submarcas = SubMarca.objects.filter(marca = marca)
    data = serializers.serialize('json', submarcas, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

def nuevo_cliente(request):
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            cliente = formulario.save()
            return HttpResponseRedirect('/listar_cliente')
    else:
        formulario = ClienteForm()
    return render_to_response('clientes/nuevo_cliente.html', {'formulario': formulario}, context_instance=RequestContext(request))

def listar_cliente(request):
    clientes = Cliente.objects.filter()
    return render_to_response('clientes/listar_cliente.html', {'clientes': clientes}, context_instance=RequestContext(request))

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
            return HttpResponseRedirect('/listar_cliente')
    else:
        formulario = ClienteForm(initial={'nombres': cliente.nombres, 'apellidos': cliente.apellidos, 'telefono': cliente.telefono, 'email': cliente.email,
                                 'direccion_fiscal': cliente.direccion_fiscal, 'rif': cliente.rif, 'cedula': cliente.cedula})
    return render_to_response('clientes/nuevo_cliente.html', {'formulario': formulario}, context_instance=RequestContext(request))

def eliminar_cliente(request, id_cliente):
    cliente = Cliente.objects.get(id=id_cliente).delete()
    return HttpResponseRedirect('/listar_cliente')

def agregar_sede_macrocliente_ajax(request):
    if Direccion.objects.filter(direccion = request.GET['direc']).count() == 0:
        dirc = 0
        data = json.dumps({'status': dirc})
    else:
        dirc = 1
        data = json.dumps({'status': dirc})
    return HttpResponse(data, mimetype='application/json')
