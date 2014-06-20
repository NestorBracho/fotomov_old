import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage, EmailMultiAlternatives
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
from modulo_movil.forms import ArchivoForm, IngresarTicketForm
from evento.models import *
from clientes.models import *
from productos.models import *
import csv
import time as tm
from datetime import *
import os
from os.path import exists
from os import makedirs
from django.conf import settings
from os import listdir
from os.path import isfile, join, isdir
from datetime import *
import datetime
import shutil
#from escpos import *
from django.core.management import call_command
from django.forms.formsets import formset_factory
from django.utils import simplejson
from unicodedata import normalize
from modulo_movil.forms import *



def ingresar(request):
    if request.method=='POST':
	formulario = AuthenticationForm(request.POST)
	if formulario.is_valid:
	  usuario = request.POST['username']
	  clave = request.POST['password']
	  acceso = authenticate(username = usuario, password = clave)
	  if acceso is not None:
	    if acceso.is_active:
		login(request, acceso)
		return HttpResponseRedirect('/seleccionar_evento')
	    else:
		return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
	  else:
	    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
    else:
	formulario = AuthenticationForm()
    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

def ingresar_vendedor(request):
    if request.method=='POST':
	formulario = AuthenticationForm(request.POST)
	if formulario.is_valid:
	  usuario = request.POST['username']
	  clave = request.POST['password']
	  acceso = authenticate(username = usuario, password = clave)
	  if acceso is not None:
	    if acceso.is_active:
		login(request, acceso)
		return HttpResponseRedirect('/seleccionar_evento')
	    else:
		return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
	  else:
	    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
    else:
	formulario = AuthenticationForm()
    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

def ingresar_caja(request):
    if request.method=='POST':
	formulario = AuthenticationForm(request.POST)
	if formulario.is_valid:
	  usuario = request.POST['username']
	  clave = request.POST['password']
	  acceso = authenticate(username = usuario, password = clave)
	  if acceso is not None:
	    if acceso.is_active:
		login(request, acceso)
		return HttpResponseRedirect('/seleccionar_evento_caja')
	    else:
		return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
	  else:
	    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
    else:
	formulario = AuthenticationForm()
    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

def configurar_db(request):
    return render_to_response('modulo_movil/configurar_db.html', {}, context_instance=RequestContext(request))

def obtener_timestamp():
    a = tm.time()
    b = str(a).split('.')
    c = b[0] + b[1]
    return c

def date_to_int(dia):
    dia_split = str(dia).split('-')
    dia_cont = dia_split[0]
    return dia_cont

def actualizar_datos():
    clientes = cliente_aux.objects.all()
    pedidos = pedido_aux.objects.all()
    productos = ProductoEventoPedido_aux.objects.all()
    pagos = PedidoPago_aux.objects.all()
    for cliente in clientes:
        print cliente
        if Cliente.objects.filter(cedula=cliente.cedula):
            aux= Cliente.objects.get(cedula=cliente.cedula)
            aux.nombres = cliente.nombres
            aux.apellidos = cliente.apellidos
            aux.telefono = cliente.telefono
            aux.email = cliente.email
            aux.direccion_fiscal = cliente.direccion_fiscal
            aux.rif = cliente.rif
            aux.cedula = cliente.cedula
            aux.save()
            print aux.cedula
        else:
            aux = Cliente.objects.create(nombres=cliente.nombres, apellidos=cliente.apellidos, telefono=cliente.telefono, email=cliente.email,
                                   direccion_fiscal=cliente.direccion_fiscal, rif=cliente.rif, cedula=cliente.cedula)
            print aux.cedula

    for pedido in pedidos:
        print "pedido"
        titulo = "Hola! "
        contenido = "Tu numero de recibo para tu pedido de hoy es: "
        try:
            print pedido.cliente.cedula
            paver = Cliente.objects.filter(cedula='18941663')
            busca = pedido.cliente.cedula
        except:
            busca="nada"
        if Cliente.objects.filter(cedula=busca):
            cliente= Cliente.objects.get(cedula=pedido.cliente.cedula)
            titulo = titulo + cliente.nombres
            contenido = contenido + str(pedido.codigo)
            correo = EmailMessage(titulo, contenido, to=[cliente.email])
            try:
                #correo.send()
                mensaje = "The email was sent correctly"
            except:
                mensaje= 'error sending the emal'
        else:
            cliente=None
        if Pedido.objects.filter(num_pedido=pedido.num_pedido):
            pass
        else:
            try:
                envio = TipoEnvio.objects.get(id=pedido.envio)
            except:
                envio = None
            Pedido.objects.create(evento=pedido.evento, cliente=cliente, fecha=pedido.fecha, num_pedido=pedido.num_pedido, fecha_entrega=pedido.fecha_entrega,
                              id_fiscal=pedido.id_fiscal, direccion_fiscal=pedido.direccion_fiscal, tlf_fiscal=pedido.tlf_fiscal,
                              razon_social=pedido.razon_social, total=pedido.total, codigo=pedido.codigo, direccion_entrega=pedido.direccion_entrega,
                              envio=envio, fue_pagado=pedido.fue_pagado, lote=pedido.lote, estado=pedido.estado, comentario=pedido.comentario)
    for producto in productos:
        prodev= ProductoEvento.objects.get(id=producto.producto)
        ProductoEventoPedido.objects.create(cantidad=producto.cantidad, ruta=producto.ruta, num_pedido=producto.num_pedido,
                                            producto=prodev, estado=producto.estado, comentario=producto.comentario)

    for pago in pagos:
        tipo = FormaDePago.objects.get(id=pago.tipo_pago)
        PedidoPago.objects.create(num_pedido=pago.num_pedido, tipo_pago=tipo, monto=pago.monto, referencia=pago.referencia)

    return HttpResponseRedirect('/escritorio')

@login_required(login_url='/')
def importar_csv_evento(request):
    if request.method == 'POST':
        cliente_aux.objects.all().delete()
        pedido_aux.objects.all().delete()
        ProductoEventoPedido_aux.objects.all().delete()
        PedidoPago_aux.objects.all().delete()
        formulario = ArchivoForm(request.POST, request.FILES)
        if formulario.is_valid():
            file = formulario.cleaned_data['archivo']
            check = str(file).split('.')
            if check[len(check) - 1] == "csv":
                #archivo = open(file)
                manejador = csv.reader(file)
                tipo = 0
                for row in manejador:
                    print row
                    if tipo == 0:
                        try:
                            cliente = cliente_aux.objects.create(nombres=row[0], apellidos=row[1], telefono=row[2], email=row[3],
                                                             direccion_fiscal=row[4], rif=row[5], cedula=row[6])
                        except:
                            pass
                        if row[0] == '!-endcliente-!':
                            tipo = 1
                    if tipo == 1:
                        if row[0] != '!-endcliente-!':
                            try:
                                if row[0] != "None":
                                    print row[0]
                                    cl = cliente_aux.objects.get(cedula=row[0])
                                else:
                                    cl = None
                                if row[3] == "":
                                    row[3]= None
                                if row[8] == "":
                                    row[8]= None
                                pedido = pedido_aux.objects.create(cliente=cl, fecha=row[1], num_pedido=row[2], fecha_entrega=row[3],
                                                               id_fiscal=row[4], direccion_fiscal=row[5], tlf_fiscal=row[6],
                                                               razon_social=row[7], total=row[8], direccion_entrega=row[9],
                                                               envio=row[10], fue_pagado=row[11], estado=row[13], evento=Evento.objects.get(id=row[14]),
                                                               comentario = row[15])
                            except:
                                pass
                            if row[0] == '!-endpedido-!':
                                tipo = 2

                    if tipo == 2:
                        print "despues del tipo 2"

                        if row[0] != '!-endpedido-!':
                            print "im in"
                            try:
                                producto = ProductoEventoPedido_aux.objects.create(cantidad=row[0], ruta=row[1], num_pedido=row[2],
                                                                                   producto=row[3], estado=row[4], comentario=row[5])
                            except:
                                pass
                            if row[0] == '!-endproducto-!':
                                tipo = 3
                    if tipo == 3:
                        if row[0] != '!-endproducto-!':
                            try:
                                pago = PedidoPago_aux.objects.create(num_pedido=row[0], tipo_pago=row[1], monto=row[2], referencia=row[3])
                            except:
                                pass
            else:
                print False
        actualizar_datos()
    else:
        formulario = ArchivoForm()
    return render_to_response('modulo_movil/importar_csv_evento.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def exportar_csv_central(request):

    #direccion = Direccion.objects.create(nombre="superprueba3333", direccion="cualquiera", lon=2.2, lat=2.2, descripcion="cualquier")
    #direccion.save()
    #print direccion.id
    #subprocess.call(['./dump-central.sh'])
    fecha = datetime.datetime.now()
    nombre = 'db-movil.json'
    output = open(settings.MEDIA_ROOT+"/base_datos/" + nombre,'w') # Point stdout at a file for dumping data to.
    call_command('dumpdata', use_natural_keys=True,format='json',indent=3,stdout=output)
    output.close()
    return HttpResponseRedirect('/configuracion/1')

@login_required(login_url='/')
def importar_csv_central(request):

    call_command('flush', interactive= False)
    call_command('loaddata', settings.MEDIA_ROOT+"/base_datos/db-movil.json")
    return HttpResponseRedirect('/iniciar_sesion')

@login_required(login_url='/')
def exportar_csv_central2(request):

    clientes = Cliente.objects.all()
    date = datetime.datetime.now()
    fecha = str(date).split(" ")
    direcciones = Direccion.objects.all()
    funciones = Funcion.objects.filter(dia__gte=fecha[0])
    eventos = []
    for funcion in funciones:
        try:
            eventos.index(funcion.evento)
        except:
            eventos.append(funcion.evento)
    encargados=[]
    for evento in eventos:
        try:
            encargados.index(evento.encargado)
        except:
            encargados.append(evento.encargado)
    sedes = []
    for evento in eventos:
        try:
            sedes.index(evento.sede)
        except:
            sedes.append(evento.sede)

    nombre = '"db-central' + str(fecha) + '.csv"'
    response['Content-Disposition'] = 'attachment; filename=' + nombre

    writer = csv.writer(response)
    for cliente in clientes:
        writer.writerow([cliente.id, cliente.nombres, cliente.apellidos, cliente.telefono, cliente.email,
                         cliente.direccion_fiscal, cliente.rif, cliente.cedula])

    writer.writerow(['!-endcliente-!'])
    for direccion in direcciones:
        writer.writerow([direccion.id, direccion.nombre, direccion.lon, direccion.lat, direccion.descripcion])
    writer.writerow(['!-enddireccion-!'])
    for encargado in encargados:
        writer.writerow([encargado.id, encargado.nombre, encargado.cedula, encargado.cargo, encargado.telefono,
                         encargado.email, encargado.descripcion, encargado.macrocliente])
    writer.writerow(['!-endencargado-!'])
    for sede in sede:
        writer.writerow([sede.id, sede.nombre, sede.direccion, "1"])
    for evento in eventos:
        writer.writerow([evento.id, evento.nombre, evento.descripcion, evento.porcentaje_institucion,
                         evento.encargado.id, evento.encargado.id, evento.sede.id])
    for funcion in funciones:
        writer.writerow([funcion.id, funcion.evento.id, funcion.dia, funcion.horas, funcion.entrega_fotos,
                         funcion.direccion.id])
    #eventos = Evento.objects.filter
    return True

def imprimir_ticket(pedido, id_evento):
    productos = ProductoEventoPedido.objects.filter(num_pedido=pedido.num_pedido)
    pagos = PedidoPago.objects.filter(num_pedido=pedido.num_pedido)
    evento = Evento.objects.get(id=id_evento)
    iva = Configuracion.objects.get(nombre="iva")
    #evento = productos[0].producto.evento.nombre
    impresora = printer.Usb(0x1cb0,0x0003)
    impresora.text("\nRECIBO FOTOMOV\n")
    impresora.text("#: " + str(pedido.num_pedido) + "\n")
    impresora.text(evento.nombre+"\n")
    impresora.text("Fecha: " + str(date.today()) + "\n\n")
    impresora.text("Productos:\n")
    for producto in productos:
        texto = str(producto.cantidad) + " x " + str(producto.producto.producto.nombre) + " = " + str(producto.producto.precio) + "\n"
        impresora.text(texto)
    impresora.text("\n")
    subtotal = str(pedido.total/float("1." + str(iva.valor)))
    impresora.text("Subtotal: " + str('%.2f'%(float(subtotal))) + "\n")
    impresora.text("Impuesto: " + str(pedido.total*float("0." + str(iva.valor))) + "\n")
    impresora.text("Total: " +str(pedido.total)+"\n")
    for pago in pagos:
        texto = pago.tipo_pago.nombre + " " + str(pago.monto) + " Bs.\n"
        impresora.text(texto)
    impresora.text("\nTotal: " + str(pedido.total) + " Bs.\n\n")
    if pedido.envio != 0:
        impresora.text("direccion de entrega:\n")
        if pedido.envio.req_dir:
            impresora.text(str(pedido.direccion_entrega)+"\n\n")
        else:
            impresora.text(str(pedido.envio.direccion)+"\n\n")
    impresora.text("Contacto Fotomov:\n")
    impresora.text("tlf: " + ConfiguracionEmpresa.objects.get(nombre="tlf").valor +"\n")
    impresora.text("tlf: " + ConfiguracionEmpresa.objects.get(nombre="celular").valor + "\n")

    impresora.text("Instagram/Facebook = fotomov\n")
    impresora.text(ConfiguracionEmpresa.objects.get(nombre="pagina").valor +"\n")
    #impresora.text("5 x Foto10x10\n")
    #impresora.text("2 x Taza\n")
    impresora.cut()

@login_required(login_url='/')
def exportar_csv_evento(request):

    response = HttpResponse(content_type='text/csv')
    fecha = datetime.datetime.now()
    clientes = Cliente.objects.all()
    pedidos = Pedido.objects.all()
    pep = ProductoEventoPedido.objects.all()
    forma_pago = PedidoPago.objects.all()

    nombre = '"db-movil' + str(fecha) + '.csv"'
    response['Content-Disposition'] = 'attachment; filename=' + nombre

    writer = csv.writer(response)
    for cliente in clientes:
        writer.writerow([cliente.nombres, cliente.apellidos, cliente.telefono, cliente.email,
                         cliente.direccion_fiscal, cliente.rif, cliente.cedula])

    writer.writerow(['!-endcliente-!'])

    for pedido in pedidos:
        client = pedido.cliente
        try:
            client = pedido.cliente.cedula
        except:
            client = "None"
            print "tiene cedula"
        try:
            envio = pedido.envio.id
        except:
            envio = 0
        writer.writerow([client, pedido.fecha, pedido.num_pedido, pedido.fecha_entrega,
                        pedido.id_fiscal, pedido.direccion_fiscal, pedido.tlf_fiscal, pedido.razon_social,
                        pedido.total, pedido.direccion_entrega, envio,
                        pedido.fue_pagado, pedido.lote, pedido.estado, pedido.evento.id, pedido.comentario])

    writer.writerow(['!-endpedido-!'])

    for producto in pep:
        writer.writerow([producto.cantidad, producto.ruta.encode("utf-8"), producto.num_pedido,
                         producto.producto.id, producto.estado , producto.comentario])

    writer.writerow(['!-endproducto-!'])

    for forma in forma_pago:
         writer.writerow([forma.num_pedido, forma.tipo_pago.id, forma.monto, forma.referencia])

    return response

@login_required(login_url='/')
def configuracion(request, creado):

#    print settings.MEDIA_ROOT
#    settings.MEDIA_ROOT = '/home/leonardo/turpial'
#    print settings.MEDIA_ROOT
    tlf = ConfiguracionEmpresa.objects.get(nombre='tlf')
    celular = ConfiguracionEmpresa.objects.get(nombre='celular')
    iva = Configuracion.objects.get(nombre='iva')
    pagina = ConfiguracionEmpresa.objects.get(nombre='pagina')
    if request.method == 'POST':
        tlf.valor = request.POST.get('tlf')
        celular.valor = request.POST.get('celular')
        iva.valor = request.POST.get('iva')
        pagina.valor = request.POST.get('pagina')
        return HttpResponseRedirect('/escritorio')
    else:
        directorio = settings.MEDIA_ROOT
    return render_to_response('modulo_movil/seleccionar_directorio.html', {'directorio': directorio,
                                                                           'creado': creado, 'iva': iva, 'pagina': pagina,
                                                                           'tlf': tlf, 'celular': celular}, context_instance=RequestContext(request))

@login_required(login_url='/')
def selecccionar_direccion(request):
#    print settings.MEDIA_ROOT
#    settings.MEDIA_ROOT = '/home/leonardo/turpial'
#    print settings.MEDIA_ROOT
    try:
        call_command('syncdb', interactive = False)
    except:
        pass
    return HttpResponseRedirect('/modulo_movil_configurar_db')

@login_required(login_url='/')
def seleccionar_evento(request):

    direcciones = Direccion.objects.all()
    eventos = []
    if directorio_actual.objects.filter(usuario = request.user):
            dir_actual = directorio_actual.objects.get(usuario=request.user).delete()
    for direccion in direcciones:
        funciones_hoy = Funcion.objects.filter(dia=date.today(), direccion = direccion).exclude(evento__id=1)
        if funciones_hoy:
            for prueba in funciones_hoy:
                print prueba.evento.id
            eventos.append(funciones_hoy[0])
    return render_to_response('modulo_movil/seleccionar_evento.html', {'eventos': eventos}, context_instance=RequestContext(request))


@login_required(login_url='/')
def seleccionar_evento_caja(request):

    direcciones = Direccion.objects.all()
    eventos = []
    if directorio_actual.objects.filter(usuario = request.user):
            dir_actual = directorio_actual.objects.get(usuario=request.user).delete()
    for direccion in direcciones:
        funciones_hoy = Funcion.objects.filter(dia=date.today(), direccion = direccion).exclude(evento__id=1)
        if funciones_hoy:
            eventos.append(funciones_hoy[0])
    return render_to_response('modulo_movil/seleccionar_evento_caja.html', {'eventos': eventos}, context_instance=RequestContext(request))


@login_required(login_url='/')
def crear_pedidos(request, id_evento, id_funcion, next, actual):

    try:
        evento = Evento.objects.get(id=id_evento)
        funcion_aux = Funcion.objects.get(id=id_funcion)
        int_dia = date_to_int(funcion_aux.dia)
        if directorio_actual.objects.filter(usuario = request.user):
            dir_actual = directorio_actual.objects.get(usuario=request.user)
        else:
            timestamp = obtener_timestamp()
            numero_pedido = str(id_evento) + str(funcion_aux.direccion.id) + int_dia + str(timestamp)
            int_numero_pedido = int(numero_pedido)
            dir_actual = directorio_actual.objects.create(usuario=request.user, directorio = settings.MEDIA_ROOT + "/eventos/", pedido=Pedido.objects.create(num_pedido=int_numero_pedido, evento=Evento.objects.get(id=id_evento)))
        lista_agregados = []
        productos_pedidos = ProductoEventoPedido.objects.filter(num_pedido=dir_actual.pedido.num_pedido)
        for agregado in productos_pedidos:
            lista_agregados.append((agregado, agregado.ruta.split('/')[-1]))
        funciones = Funcion.objects.filter(evento=evento)
        generar_rutas(id_evento)
        separado = request.path.split('urlseparador')
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
        productos = ProductoEvento.objects.filter(evento=evento, es_combo=False)
        dir_actual.save()
        return render_to_response('modulo_movil/crear_pedidos.html', {'productos': productos, 'imagenes': imagenes, 'directorios': directorios, 'current': current, 'evento': evento,
                                                                  'short_current': short_current, 'productos_pedidos': lista_agregados,
                                                                  'dir_actual': dir_actual, 'id_funcion': id_funcion, 'MEDIA_ROOT':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
    except:
        print "exept************************************************************************************"
        next = "NoneNext"
        actual = "NoneValue"
        evento = Evento.objects.get(id=id_evento)
        funcion_aux = Funcion.objects.get(id=id_funcion)
        int_dia = date_to_int(funcion_aux.dia)
        #print directorio_actual.objects.filter(usuario = request.user)
        if directorio_actual.objects.filter(usuario = request.user):
            dir_actual = directorio_actual.objects.get(usuario=request.user)
        else:
            timestamp = obtener_timestamp()
            numero_pedido = str(id_evento) + str(funcion_aux.direccion.id) + int_dia + str(timestamp)
            int_numero_pedido = int(numero_pedido)
            dir_actual = directorio_actual.objects.create(usuario=request.user, directorio = settings.MEDIA_ROOT + "/eventos/", pedido=Pedido.objects.create(num_pedido=int_numero_pedido, evento=Evento.objects.get(id=id_evento)))
        lista_agregados = []
        productos_pedidos = ProductoEventoPedido.objects.filter(num_pedido=dir_actual.pedido.num_pedido)
        for agregado in productos_pedidos:
            lista_agregados.append((agregado, agregado.ruta.split('/')[-1]))
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
        productos = ProductoEvento.objects.filter(evento=evento, es_combo=False)
        print "que pasa ahora?"
        print productos
        dir_actual.save()
        return render_to_response('modulo_movil/crear_pedidos.html', {'productos': productos, 'imagenes': imagenes, 'directorios': directorios, 'current': current, 'evento': evento,
                                                                  'short_current': short_current, 'productos_pedidos': lista_agregados,
                                                                  'dir_actual': dir_actual, 'id_funcion': id_funcion, 'MEDIA_ROOT':settings.MEDIA_ROOT}, context_instance=RequestContext(request))

@login_required(login_url='/')
def crear_pedidos_indoor(request, id_evento, id_funcion, next, actual):

    try:
        evento = Evento.objects.get(id=id_evento)
        funcion_aux = Funcion.objects.get(id=id_funcion)
        int_dia = date_to_int(funcion_aux.dia)
        if directorio_actual.objects.filter(usuario = request.user):
            dir_actual = directorio_actual.objects.get(usuario=request.user)
        else:
            timestamp = obtener_timestamp()
            numero_pedido = str(id_evento) + str(funcion_aux.direccion.id) + int_dia + str(timestamp)
            int_numero_pedido = int(numero_pedido)
            dir_actual = directorio_actual.objects.create(usuario=request.user, directorio = settings.MEDIA_ROOT + "/eventos/", pedido=Pedido.objects.create(num_pedido=int_numero_pedido, evento=Evento.objects.get(id=id_evento)))
        lista_agregados = []
        productos_pedidos = ProductoEventoPedido.objects.filter(num_pedido=dir_actual.pedido.num_pedido)
        for agregado in productos_pedidos:
            lista_agregados.append((agregado, agregado.ruta.split('/')[-1]))
        funciones = Funcion.objects.filter(evento=evento)
        separado = request.path.split('urlseparador')
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
        productos = ProductoEvento.objects.filter(evento=evento, es_combo=False)
        dir_actual.save()
        return render_to_response('modulo_movil/crear_pedidos.html', {'productos': productos, 'imagenes': imagenes, 'directorios': directorios, 'current': current, 'evento': evento,
                                                                  'short_current': short_current, 'productos_pedidos': lista_agregados,
                                                                  'dir_actual': dir_actual, 'id_funcion': id_funcion, 'MEDIA_ROOT':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
    except:
        print "exept************************************************************************************"
        next = "NoneNext"
        actual = "NoneValue"
        evento = Evento.objects.get(id=id_evento)
        funcion_aux = Funcion.objects.get(id=id_funcion)
        int_dia = date_to_int(funcion_aux.dia)
        #print directorio_actual.objects.filter(usuario = request.user)
        if directorio_actual.objects.filter(usuario = request.user):
            dir_actual = directorio_actual.objects.get(usuario=request.user)
        else:
            timestamp = obtener_timestamp()
            numero_pedido = str(id_evento) + str(funcion_aux.direccion.id) + int_dia + str(timestamp)
            int_numero_pedido = int(numero_pedido)
            dir_actual = directorio_actual.objects.create(usuario=request.user, directorio = settings.MEDIA_ROOT + "/eventos/", pedido=Pedido.objects.create(num_pedido=int_numero_pedido, evento=Evento.objects.get(id=id_evento)))
        lista_agregados = []
        productos_pedidos = ProductoEventoPedido.objects.filter(num_pedido=dir_actual.pedido.num_pedido)
        for agregado in productos_pedidos:
            lista_agregados.append((agregado, agregado.ruta.split('/')[-1]))
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
        productos = ProductoEvento.objects.filter(evento=evento, es_combo=False)
        dir_actual.save()
        return render_to_response('modulo_movil/crear_pedidos.html', {'productos': productos, 'imagenes': imagenes, 'directorios': directorios, 'current': current, 'evento': evento,
                                                                  'short_current': short_current, 'productos_pedidos': lista_agregados,
                                                                  'dir_actual': dir_actual, 'id_funcion': id_funcion, 'MEDIA_ROOT':settings.MEDIA_ROOT}, context_instance=RequestContext(request))

def generar_rutas(id_evento):
    lista = []
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    year = str(date.today().year)

    for funcion in funciones:
        direccion = direccionFuncion.objects.get(funcion=funcion)
        ruta = settings.MEDIA_ROOT + '/eventos/' + year + '/' + direccion.dir
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        #print ruta
        lista.append(ruta)
    return lista

@login_required(login_url='/')
def agregar_item(request):
    pedido = Pedido.objects.get(id=request.GET.get('id_pedido'))
    cantidad = request.GET.get('cantidad')
    comentario = request.GET.get('comentario')
    producto = ProductoEvento.objects.get(id=request.GET.get('producto'))
    imagen = request.GET.get('imagen')

    dir_actual = directorio_actual.objects.get(usuario=request.user)

    productoevento = ProductoEventoPedido.objects.create(
            comentario=comentario, cantidad=cantidad, producto=producto,
            ruta=dir_actual.directorio + imagen, num_pedido=pedido.num_pedido
        )

    prodevento = []
    prodevento.append(productoevento)

    data = serializers.serialize('json', prodevento,
                                 fields =('cantidad', 'imagen', 'comentario', 'producto, id'))

    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def eliminar_ProductoEventoPedido(request, id, id_funcion):

    proevped = ProductoEventoPedido.objects.get(id=id)
    evento = proevped.producto.evento
    funcion = Funcion.objects.get(id=id_funcion)
    proevped.delete()
    url = "/crear_pedidos/" + str(evento.id) + "/" + str(funcion.direccion.id) + "/NoneNext/urlseparador/NoneValue/"
    return HttpResponseRedirect(url)

@login_required(login_url='/')
def generar_lote(request):

    pedidos = Pedido.objects.filter(fue_pagado = True, lote = None)
    print pedidos
    for pedido in pedidos:
        print pedido.num_pedido
    hora = str(datetime.datetime.today().day)+str(datetime.datetime.today().month)+str(datetime.datetime.today().year)+str(datetime.datetime.today().hour)+str(datetime.datetime.today().minute)
    rutalote = ''
    for pedido in pedidos:
        if pedido.cliente != None:
            peps = ProductoEventoPedido.objects.filter(num_pedido = pedido.num_pedido, producto__es_combo=False)
            print peps
            for pep in peps:
                print pep.producto.es_combo
                nom = pedido.cliente.nombres.split(' ')
                nom = nom[0]
                ape = pedido.cliente.apellidos.split(' ')
                ape = ape[0]
                client = ape + nom
                ruta = settings.MEDIA_ROOT + "/lotes/"  + pep.producto.evento.nombre + '-' + hora + '/' + client + '-' + str(pedido.num_pedido) + '/'
                rutalote = settings.MEDIA_ROOT + "/lotes/"  + pep.producto.evento.nombre + '-' + hora + '/'
                if not os.path.exists(rutalote):
                    os.makedirs(rutalote)
                    lote = Lote.objects.create(estado = 'Edicion', fecha = date.today(), ruta = rutalote, codigo = pep.producto.evento.nombre + '-' + hora)
                    lote.save()
                if pedido.lote == None:
                    pedido.lote = lote
                    pedido.save()
            productos = ProductoEventoPedido.objects.filter(num_pedido = pedido.num_pedido)
            for producto in productos:
                if not os.path.exists(ruta + producto.producto.producto.nombre + '.' + str(producto.id) + '/'):
                    os.makedirs(ruta + producto.producto.producto.nombre + '.' + str(producto.id) + '/')
                for i in range(producto.cantidad):
                    auxr = producto.ruta.split('/')
                    auxr = auxr[(len(auxr)-1)]
                    auxr = auxr.split('.')
                    auxr = auxr[0]
                    try:
                        shutil.copy(normalize('NFKD', producto.ruta).encode('ascii', 'ignore') + ruta + producto.producto.producto.nombre + '.' + str(producto.id) + '/' + auxr + '.' + str(i+1) + '.jpg')
                    except:
                        pass
            pep.estado = "Edicion"
            pep.save()
        pedido.estado = "Edicion"
        pedido.save()
    return HttpResponseRedirect('/escritorio/')

@login_required(login_url='/')
def generar_pedido(request, pedido, cedula, id_evento):

    pagosForms = formset_factory(PedidoPagoForm)
    pedido_actual = Pedido.objects.get(id=pedido)
    tipos_pago = FormaDePago.objects.all()
    print tipos_pago
    peps = ProductoEventoPedido.objects.filter(num_pedido = pedido_actual.num_pedido)
    combos = []
    productos = []

    # Construir json de tipos de pagodef generar_pedido
    tipos_envio = {}
    for tipo_envio in TipoEnvio.objects.all() :
        print tipo_envio.direccion
        tipos_envio[ tipo_envio.id ] = {
            'precio'  : str(tipo_envio.precio),
            'tipo'    : tipo_envio.tipo,
            'id'      : tipo_envio.id,
            'req_dir' : tipo_envio.req_dir,
        }

    tipos_envio = json.dumps(tipos_envio)
    print tipos_envio
    # Se busca cuales de los productos del pedido son combos
    for pep in peps:
        if pep.producto.es_combo:
            combos.append(pep)
        else:
            productos.append(pep)
    # A esos combos se les busca que productos y cuandos estan incluidos en el combo
    for combo in combos:
        combo.productos = ProductoeventoCombo.objects.filter(combo=combo.producto)
    iva = Configuracion.objects.get(nombre='iva')
    en_venta = ProductoEvento.objects.filter(evento__id=id_evento)
    print ("hooola", id_evento, en_venta)
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
    if request.method == 'POST':
        print "estoy en el poast"
        formulario = PedidoCajaForm(request.POST)
        formulario_pagos = pagosForms(request.POST)
        if formulario.is_valid():
            print "caja form es valido"
            if formulario_pagos.is_valid():
                pass
            else:
                print "los pagos no son validos"
                mensaje = {"error":1,"text": "Todos los campos del metodo de pago deben estar llenos"}
                return render_to_response('modulo_movil/generar_pedido.html', {'formulario': formulario, 'cliente': cliente,
                                                                   'productos': productos, 'combos': combos, 'ced': cedula,
                                                                   'pedido_actual': pedido_actual,
                                                                   'tipos_pago': tipos_pago, 'pagosForms': formulario_pagos,
                                                                   'mensaje': mensaje, 'en_venta': en_venta, 'iva': iva,
                                                                   'tipos_envio': tipos_envio},
                              context_instance=RequestContext(request))
            print len(formulario_pagos)
            pedidos_pagos = PedidoPago.objects.filter(num_pedido=pedido_actual.num_pedido).delete()
            pagado = True
            for form in formulario_pagos:
                try:
                    tipo_pago = FormaDePago.objects.get(id=form.cleaned_data['tipo_pago'])
                except:
                    continue
                if not tipo_pago.pagado:
                    pagado = False
                monto = form.cleaned_data['monto']
                nuevo_pago = PedidoPago.objects.create(num_pedido=pedido_actual.num_pedido, tipo_pago=tipo_pago,
                                               monto=float(monto), referencia = form.cleaned_data['referencia'])

            dia = date.today()
            #aux = str(datetime.datetime.today())
            #aux = aux.split(' ')
            cod = ''
            #for au in aux:
            #    cod = cod + au
            #aux = cod.split('-')
            #cod = ''
            #for au in aux:
            #    cod = cod + au
            #aux = cod.split(':')
            #cod = ''
            #for au in aux:
            #    cod = cod + au
            #aux = cod.split('.')
            #cod = ''
            #for au in aux:
            #    cod = cod + au
            aux = []
            #fechas_entrega = Funcion.objects.filter(evento = peps[0].producto.evento)
            #for fecha_entrega in fechas_entrega:
            #    aux.append(fecha_entrega.dia)
            #for i in range(len(aux)):
            #    if i != len(aux)-1:
            #        if aux[i+1] > aux[i]:
            #            dia = aux[i+1]
            #fecha_entrega = dia + datetime.timedelta(days = 15)
            pedido_nuevo = Pedido.objects.filter(id=pedido)
            print request.POST.get('direccion_entrega')
            print request.POST.get('total_input')
            envio = TipoEnvio.objects.get(id=formulario.cleaned_data['envio'])
            pedido_nuevo.update(cliente = cliente, fecha = date.today(), fecha_entrega = Evento.objects.get(id=id_evento).fecha_entrega,
                                id_fiscal = formulario.cleaned_data['id_fiscal'], direccion_fiscal = formulario.cleaned_data['direccion_fiscal'],
                                tlf_fiscal = formulario.cleaned_data['tlf_fiscal'], razon_social = formulario.cleaned_data['razon_social'],
                                total = request.POST.get('total_input'), descuento = request.POST.get('descuento_input'),
                                direccion_entrega = request.POST.get('direccion_entrega'), comentario=formulario.cleaned_data['comentario'],
                                fue_pagado = pagado, envio=envio)
            print "update de pedido"
            pedido_nuevo = pedido_nuevo[0]
            if pedido_nuevo.fue_pagado == True:
                for pep in peps:
                    pep.estado = 'Pagado'
                    pep.save()
            #try:
#            imprimir_ticket(pedido_nuevo, id_evento)
            #except:
            #    print "impresora desconectada"
            return HttpResponseRedirect('/ingresar_ticket/' + id_evento)
        print "sali del post sin valid"
    else:

        formulario = PedidoCajaForm(instance=pedido_actual)
        print "estoy en el else"
    return render_to_response('modulo_movil/generar_pedido.html', {'formulario': formulario, 'cliente': cliente,
                                                                   'productos': productos, 'combos': combos, 'ced': cedula,
                                                                   'pedido_actual': pedido_actual,
                                                                   'tipos_pago': tipos_pago, 'pagosForms': pagosForms,
                                                                   'en_venta': en_venta, 'iva': iva, 'tipos_envio': tipos_envio},
                              context_instance=RequestContext(request))


@login_required(login_url='/')
def ingresar_ticket(request, id_evento):
    if request.method == 'POST':
        formulario = IngresarTicketForm(request.POST)
        if formulario.is_valid():
            return HttpResponseRedirect('/generar_pedido/'+str(formulario.cleaned_data['ticket'])+'/'+str(formulario.cleaned_data['cedula'])+'/'+id_evento)
    else:
        formulario = IngresarTicketForm()
    return render_to_response('modulo_movil/ingresar_ticket.html', {'formulario': formulario}, context_instance=RequestContext(request))


def eliminar_productoeventopedido_en_generarpedido(request):
    pep = ProductoEventoPedido.objects.get(id = request.GET['iden'])
    pep.delete()
    data = json.dumps({'status': "hola"})
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def generar_ticket(request, id_evento, id_funcion):
    evento = Evento.objects.get(id=id_evento)
    info = directorio_actual.objects.get(usuario= request.user)
    funcion_aux = Funcion.objects.get(id=id_funcion)
    int_dia = date_to_int(funcion_aux.dia)
    pedido = info.pedido
    lista_agregados = []
    productos_pedidos = ProductoEventoPedido.objects.filter(num_pedido=pedido.num_pedido)
    for agregado in productos_pedidos:
        lista_agregados.append((agregado, agregado.ruta.split('/')[-1]))
    if request.method == 'POST':
        if '_Nuevo' in request.POST:
            timestamp = obtener_timestamp()
            numero_pedido = str(id_evento) + str(funcion_aux.direccion.id) + int_dia + str(timestamp)
            int_numero_pedido = int(numero_pedido)
            new = Pedido.objects.create(num_pedido=int_numero_pedido, evento=evento)
            new.save()
            info.pedido = new
            info.save()
            return HttpResponseRedirect('/crear_pedidos/'+ id_evento + "/" + id_funcion +'/NoneNext/urlseparador/NoneValue/')
        elif '_Cancelar' in request.POST:
            return HttpResponseRedirect('/crear_pedidos/'+ id_evento + "/" + id_funcion +'/NoneNext/urlseparador/NoneValue/')
    #return HttpResponseRedirect('/crear_pedidos/'+ id_evento +'/NoneNext/urlseparador/NoneValue/')
    return render_to_response('modulo_movil/generar_ticket.html', {'id_evento': id_evento, 'pedido': pedido, 'productos': lista_agregados}, context_instance=RequestContext(request))

@login_required(login_url='/')
def asignar_combos(request, id_evento, id_funcion, id_pedio):
    info = directorio_actual.objects.get(usuario= request.user)
    evento = Evento.objects.get(id = id_evento)
    pedido = info.pedido
    productos = ProductoEventoPedido.objects.filter(num_pedido=pedido.num_pedido)
    combos = ProductoEvento.objects.filter(evento = evento, es_combo = True)
    productosCliente=[]#--------------------->son los productos q esta comprando el cliente
    combosPosibles=[]#-------------------->son los combos posibles q puede comprar
    tempProd = []
    tempCant = []

    for producto in productos:
        index = False

        try:
            index = tempProd.index([producto.producto, producto.producto.id, producto.producto.precio])
        except:
            tempProd.append([producto.producto, producto.producto.id, producto.producto.precio])
            tempCant.append(producto.cantidad)
        else:
            tempCant[index] = int(tempCant[index])+int(producto.cantidad)

    productos = zip(tempProd, tempCant)

    for combo in combos:
        productosCombo = ProductoeventoCombo.objects.filter(combo = combo)
        esAplicable = True

        for prodCombo in productosCombo:

            try:
                index = tempProd.index([prodCombo.producto, prodCombo.producto.id, producto.producto.precio])
            except:
                esAplicable = False
                break
            else:
                if prodCombo.cantidad > tempCant[index]:
                    esAplicable = False
                    break

        if esAplicable :
            combosPosibles.append(combo)

    aux=[]
    productoCombos = []
    for combo in combos:
        aux.append(ProductoeventoCombo.objects.filter(combo=combo))
    for au in aux:
        for a in au:
            productoCombos.append(a)
    return render_to_response('modulo_movil/asignar_combos.html', {'productos': productos, 'combos': combosPosibles, 'productoCombos': productoCombos, 'dir_actual': info.pedido.id, 'evento': id_evento, 'funcion': id_funcion}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    productos = ProductoEventoPedido.objects.filter(num_pedido = pedido.num_pedido)
    if request.method == 'POST':
        form = PedidoReducidoForm(request.POST, instance = pedido)
        if form.is_valid():
            pedido = form.save()
            pedido.save()
            return HttpResponseRedirect('/ver_pedido/'+pedido_id+'/')
    else :
        form = PedidoReducidoForm(instance = pedido)
    return render_to_response('modulo_movil/editar_pedido.html', {'pedido': pedido, 'form': form, 'productos': productos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_pedido(request, pedido):
    pedido = Pedido.objects.get(id = pedido)
    pedido.delete()
    return HttpResponseRedirect('/listar_pedidos/')
