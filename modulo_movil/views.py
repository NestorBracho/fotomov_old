from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from evento.forms import *
from productos.forms import *
from modulo_movil.models import *
from evento.models import *
from productos.models import *
import csv
import time
from datetime import date
import os
from os.path import exists
from os import makedirs
from django.conf import settings
from os import listdir
from os.path import isfile, join, isdir
from datetime import *
import datetime
import shutil

def exportar_csv_evento(request):
    eventos = Evento.objects.all().order_by('-id')
    if request.method == 'POST':
        pass
       # exportar = request.POST.getlist('eventos')
       # nombre = "BDD-" + time.strftime("%d/%m/%Y") + ".csv"
       # archivo = open(nombre,"w+")
       # print nombre
    else:
        pass
    return render_to_response('modulo_movil/exportar_csv_evento.html', {'eventos': eventos},
                              context_instance=RequestContext(request))

def selecccionar_direccion(request):
#    print settings.MEDIA_ROOT
#    settings.MEDIA_ROOT = '/home/leonardo/turpial'
#    print settings.MEDIA_ROOT
    if request.method == 'POST':
        directorio = request.POST.get('directorio')
        settings.MEDIA_ROOT = directorio
        print settings.MEDIA_ROOT
        return HttpResponseRedirect('/escritorio')
    return render_to_response('modulo_movil/seleccionar_directorio.html', {}, context_instance=RequestContext(request))

@login_required(login_url='/')
def crear_pedidos(request, id_evento, next, actual):
    print next
    #print directorio_actual.objects.filter(usuario = request.user)
    if directorio_actual.objects.filter(usuario = request.user):
        dir_actual = directorio_actual.objects.get(usuario=request.user)
    else:
        dir_actual = directorio_actual.objects.create(usuario=request.user, directorio = settings.MEDIA_ROOT + "/eventos/")
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    generar_rutas(id_evento)
    print "aqui"
    print dir_actual.directorio
    separado = request.path.split('urlseparador')
    print separado
    year = str(date.today().year)
    if actual == "NoneValue":
        print "NoneValue"
        current = dir_actual.directorio
    elif actual == "ir":
        split_auxiliar = next.split(" ")
        print len(split_auxiliar)
        if len(split_auxiliar) > 1:
            print "entre"
            #i=0
            #concatenar = ""
            #while i < len(split_auxiliar) - 1:
            #    concatenar = concatenar + split_auxiliar[i] + "\"
            #    i = i + 1
            #next = concatenar
            print "el nuevo next es =" + next
        auxiliar = dir_actual.directorio
        dir_actual.directorio = auxiliar + next + "/"
        dir_actual.save()
        current = dir_actual.directorio
    elif actual == "back":
        auxiliar = dir_actual.directorio.split("/")
        i = 0
        print "antes del while"
        concatenar = ""
        while i < len(auxiliar) - 2:
            if i == 0:
                concatenar = concatenar + auxiliar[i]
            else:
                concatenar = concatenar + "/" + auxiliar[i]
            print auxiliar[i]
            i= i + 1
        dir_actual.directorio = concatenar + "/"
        dir_actual.save()
        current = dir_actual.directorio
    else:
        print "estoy en el else"
        current = settings.MEDIA_ROOT + "/eventos/" + year + "" + separado[1]
        print "sali del else"
    print "aqui va el current"
    print current
    short_current = current.split("fotomov_imagenes")[1]
    print "aqui va el short"
    print short_current
    lista_imagenes = []
    imagenes = [ f for f in listdir(current) if isfile(join(current,f)) ]
    for imagen in imagenes:
        dividir_url = imagen.split("fotomov_imagenes")
    directorios = [ f for f in listdir(current) if isdir(join(current,f)) ]
    print imagenes
    print directorios
    if request.method == 'POST':
        pass
    return render_to_response('modulo_movil/crear_pedidos.html', {'imagenes': imagenes, 'directorios': directorios, 'current': current, 'evento': evento, 'short_current': short_current}, context_instance=RequestContext(request))

def generar_rutas(id_evento):
    lista = []
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    year = str(date.today().year)

    for funcion in funciones:
        direccion = direccionFuncion.objects.get(funcion=funcion)
        ruta = settings.MEDIA_ROOT + "/eventos/" + year + '/' + direccion.dir
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        #print ruta
        lista.append(ruta)
    return lista

def generar_lote(request):#rehacer
    pedidos = Pedido.objects.filter(fue_pagado = True, lote = None)
    hora = str(datetime.datetime.today().day)+str(datetime.datetime.today().month)+str(datetime.datetime.today().year)+str(datetime.datetime.today().hour)+str(datetime.datetime.today().minute)
    rutalote = ''
    for pedido in pedidos:
        peps = ProductoEventoPedido.objects.filter(pedido = pedido)
        for pep in peps:
            nom = pedido.cliente.nombres.split(' ')
            nom = nom[0]
            ape = pedido.cliente.apellidos.split(' ')
            ape = ape[0]
            client = ape + nom
            ruta = settings.MEDIA_ROOT + "/lotes/"  + pep.producto.evento.nombre + '-' + hora + '/' + client + '-' + pedido.codigo + '/'
            rutalote = settings.MEDIA_ROOT + "/lotes/"  + pep.producto.evento.nombre + '-' + hora + '/'
            if not os.path.exists(rutalote):
                os.makedirs(rutalote)
                lote = Lote.objects.create(estado = 'creado', fecha = date.today(), ruta = rutalote, codigo = pep.producto.evento.nombre + '-' + hora)
                lote.save()
            if not os.path.exists(ruta):
                os.makedirs(ruta)
            productos = ProductoEventoPedido.objects.filter(pedido = pedido)
            for producto in productos:
                for i in range(producto.cantidad):
                    shutil.copy(pep.ruta, ruta+producto.producto.producto.nombre + '.' + str(i+1) + '.jpg')
    return HttpResponseRedirect('/escritorio/')

def generar_pedido(request, pedido, cedula):
    peps = ProductoEventoPedido.objects.filter(num_pedido = pedido)
    cliente = Cliente.objects.filter(cedula = cedula)
    if len(cliente) > 0:
        cliente = cliente[0]
    else:
        cliente = None
        if request.method == 'POST':
            nom = request.POST['nombres_cliente']
            ape = request.POST['apellidos_cliente']
            tlf = request.POST['telefono_cliente']
            mail = request.POST['mail_cliente']
            direc = request.POST['direccion_fiscal_cliente']
            rif = request.POST['rif_cliente']
            ced = request.POST['cedula_cliente']
            cliente = Cliente.objects.create(nombres = nom, apellidos = ape, telefono = tlf, email = mail, direccion_fiscal = direc, rif = rif, cedula = ced)
    formulario = PedidoForm()
    if request.method == 'POST':
        formulario = PedidoForm(request.POST)
        aux = str(datetime.datetime.today())
        aux = aux.split(' ')
        cod = ''
        for au in aux:
            cod = cod + au
        aux = cod.split('-')
        cod = ''
        for au in aux:
            cod = cod + au
        aux = cod.split(':')
        cod = ''
        for au in aux:
            cod = cod + au
        aux = cod.split('.')
        cod = ''
        for au in aux:
            cod = cod + au
        aux = []
        fechas_entrega = Funcion.objects.filter(evento = peps[0].producto.evento)
        for fecha_entrega in fechas_entrega:
            aux.append(fecha_entrega.dia)
        for i in range(len(aux)):
            if i != len(aux)-1:
                if aux[i+1] > aux[i]:
                    dia = aux[i+1]
        fecha_entrega = dia + datetime.timedelta(days = 15)
        try:
            if request.POST['fue_pagado']:
                pagado = True
        except:
            pagado = False
        pedido_nuevo = Pedido.objects.create(cliente = cliente, fecha = date.today(), fecha_entrega = fecha_entrega, id_fiscal = request.POST['id_fiscal'], direccion_fiscal = request.POST['direccion_fiscal'], tlf_fiscal = request.POST['tlf_fiscal'], razon_social = request.POST['razon_social'], total = request.POST['total'], codigo = cod, direccion_entrega = request.POST['direccion_entrega'], fue_pagado = pagado)
        pedido_nuevo.save()
        for pep in peps:
            pep.pedido = pedido_nuevo
            pep.save()
        return HttpResponseRedirect('/ingresar_ticket/'+cod+'/')
    return render_to_response('modulo_movil/generar_pedido.html', {'formulario': formulario, 'cliente': cliente, 'pedidos': peps, 'ced': cedula}, context_instance=RequestContext(request))

def ingresar_ticket(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/generar_pedido/'+request.POST['numero']+'/'+request.POST['cedula_cliente'])
    return render_to_response('modulo_movil/ingresar_ticket.html', {}, context_instance=RequestContext(request))