# -*- encoding: utf-8 -*-
import json
import csv
import time
from django.utils import simplejson
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
from marca.views import Marca, SubMarca
from direcciones.views import *
from tareas.models import *
from modulo_movil.models import *
from datetime import *
from django.core.mail import send_mail
from django.contrib import messages
import datetime

@login_required(login_url='/')
def nuevo_evento(request):
    gastos_predeterminados = Gasto.objects.filter(predeterminado = True)
    direcciones = obtener_direcciones()
    if request.method == 'POST':
        formulario = EventoForm(request.POST)
        if formulario.is_valid():
            tipo_cliente = request.POST.get('seleccionar_tipo')
            dias = request.POST.getlist('dias')
            if len(dias) <= 0:
                mensaje_dias = 1
                return render_to_response('evento/nuevo_evento.html', {'formulario': formulario,
                                                                       'gastos': gastos_predeterminados, 'direcciones': direcciones, 'mensaje_dias': mensaje_dias}, context_instance = RequestContext(request))
            entrega_final = formulario.cleaned_data['fecha_entrega']
            #print fecha_entrega
            #entrega_split = str(fecha_entrega).split('-')
            #print entrega_split
            #entrega_final = entrega_split[2] + "-" + entrega_split[1] + "-" + entrega_split[0]
            print "tipo de cliente para el evento"
            print request.POST.get('seleccionar_tipo')
            if tipo_cliente == 'm':
                encargado = Encargado.objects.get(id=request.POST.get('encargado'))
                sede = Sede.objects.get(id=request.POST.get('sede'))
                evento = Evento.objects.create(nombre=formulario.cleaned_data['nombre'], descripcion=formulario.cleaned_data['descripcion'],
                                               porcentaje_institucion=formulario.cleaned_data['porcentaje_institucion'], encargado=encargado,
                                               sede=sede, tipo=formulario.cleaned_data['tipo'], macrocliente=formulario.cleaned_data['macrocliente'],
                                               fecha_entrega=entrega_final, submarca=formulario.cleaned_data['macrocliente'].submarca)
            else:
                cliente = str(request.POST.get('cliente')).split('-')
                try:
                    cliente_evento = Cliente.objects.get(cedula=cliente[1])
                except:
                    return render_to_response('evento/nuevo_evento.html', {'formulario': formulario, 'gastos': gastos_predeterminados, 'direcciones': direcciones}, context_instance = RequestContext(request))
                evento = Evento.objects.create(cliente= cliente_evento, nombre=formulario.cleaned_data['nombre'], descripcion=formulario.cleaned_data['descripcion'],
                                               porcentaje_institucion=formulario.cleaned_data['porcentaje_institucion'],
                                               tipo=formulario.cleaned_data['tipo'], fecha_entrega=entrega_final, submarca=SubMarca.objects.get(id=request.POST.get('submarca')))
            print dias
            if len(dias) > 0:
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
                            if tipo_cliente == 'm':
                                directorio = direccionFuncion.objects.create(funcion=funcion_save, dir = funcion_save.evento.macrocliente.submarca.marca.nombre + "/" + funcion_save.evento.macrocliente.submarca.nombre + "/" + funcion_save.evento.macrocliente.nombre + "/" + funcion_save.evento.nombre + "/" + funcion_save.evento.sede.nombre + "/" + funcion_save.dia + "/" + funcion_save.direccion.nombre + "/" +funcion_save.nombre)
                            else:
                                directorio = direccionFuncion.objects.create(funcion=funcion_save, dir = funcion_save.evento.submarca.marca.nombre + "/" + funcion_save.evento.submarca.nombre + "/" + funcion_save.evento.cliente.nombres + funcion_save.evento.cliente.apellidos + "/" + funcion_save.evento.nombre + "/" + funcion_save.dia + "/" + funcion_save.direccion.nombre + "/" +funcion_save.nombre)
            #Empieza a crear las tareas del evento
            tareas = TareaTipoEvento.objects.filter(tipo_evento=evento.tipo)
            fechas = Funcion.objects.filter(evento=evento).order_by('dia')

            fecha_ini = fechas[0].dia
            fecha_fin = fechas[len(fechas) - 1].dia
            prueba_antes = fecha_ini - datetime.timedelta(days=2)

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

@login_required(login_url='/')
def agregar_staff(request, id_evento):
    bloques = Bloque.objects.all().order_by("nombre")
    evento = Evento.objects.get(id=id_evento)
    funciones = Funcion.objects.filter(evento=evento)
    tipos_staff = Privilegios.objects.filter(valor=6)
    lista = []
    for funcion in funciones:
        staff = StaffPorFuncion.objects.filter(funcion=funcion)
        if len(staff) == len(tipos_staff):
            tupla = (funcion,staff)
            lista.append(tupla)
        else:
            van = []
            for tipo in tipos_staff:

                if StaffPorFuncion.objects.filter(funcion=funcion, tipo=tipo):
                     creado = StaffPorFuncion.objects.get(funcion=funcion, tipo=tipo)
                else:
                    creado = StaffPorFuncion.objects.create(tipo=tipo, funcion=funcion, cantidad=0)
                    van.append(creado)
            tupla = (funcion,staff)
            lista.append(tupla)
    if request.method == 'POST':
        for funcion in funciones:
            for staff in tipos_staff:
                print str(funcion.id) + "-" + str(staff.id)
                print request.POST.get(str(funcion.id) + "-" + str(staff.id))
                cantidad = request.POST.get(str(funcion.id) + "-" + str(staff.id))
                agregar = StaffPorFuncion.objects.get(tipo=staff, funcion=funcion)
                if cantidad != None:
                    print "aja"
                    agregar.cantidad = cantidad
                if request.POST.get("bloque-" + str(funcion.id) + "-" + str(staff.id)) != "None":
                    agregar.bloque = Bloque.objects.get(id = request.POST.get("bloque-" + str(funcion.id) + "-" + str(staff.id)))
                agregar.save()
        return HttpResponseRedirect("/listar_evento/2")
    print lista
    return render_to_response('evento/agregar_staff.html', {'funciones': lista, 'evento': evento, 'bloques':bloques}, context_instance= RequestContext(request))


def encargado_ajax(request):
    macroC = MacroCliente.objects.get(id=request.GET['id'])
    contacto = Encargado.objects.filter(macrocliente=macroC)
    data = serializers.serialize('json', contacto, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

def submarca_ajax(request):
    marca = Marca.objects.get(id=request.GET['id'])
    submarca = SubMarca.objects.filter(marca=marca)
    data = serializers.serialize('json', submarca, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

def sede_ajax(request):
    macroC = MacroCliente.objects.get(id=request.GET['id'])
    contacto = Sede.objects.filter(macrocliente=macroC)
    data = serializers.serialize('json', contacto, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def listar_evento(request, creado):
    eventos = Evento.objects.all().exclude(id=1)
    return render_to_response('evento/listar_evento.html', {'eventos': eventos, 'creado': creado}, context_instance = RequestContext(request))

def locacion_ajax(request):
    locaciones = Direccion.objects.filter(nombre__contains=request.GET['locacion']).exclude(id=1)
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

@login_required(login_url='/')
def agregar_productos(request,id_evento):
    productos = Producto.objects.all().exclude(es_combo=True)
    evento = Evento.objects.get(id=id_evento)
    proveedores = Proveedor.objects.all()
    lista = []
    for producto in productos:
        if ProductoEvento.objects.filter(evento=evento, producto=producto):
            producto_existente = ProductoEvento.objects.get(evento=evento, producto=producto)
            tupla=(producto, 1, producto_existente.precio, producto_existente.precio_produccion, producto_existente.proveedor)
        else:
            tupla = (producto, 0, 0, 0)
        lista.append(tupla)

    if request.method == 'POST':
        seleccionados = request.POST.getlist('seleccionados')
        existentes = ProductoEvento.objects.filter(evento=evento)
        #for existente in existentes:
            #existente.delete()
        for seleccionado in seleccionados:
            precio = request.POST.get(seleccionado+'precio')
            costo = request.POST.get(seleccionado+'costo')
            proveedor = request.POST.get(seleccionado+'proveedor')
            proveedor = Proveedor.objects.get(id = proveedor)
            producto = Producto.objects.get(id=seleccionado)
            try:
                producto_evento = ProductoEvento.objects.get(producto=producto, evento=evento)
                producto_evento.precio= float(precio.replace(',','.'))
                producto_evento.precio_produccion = float(costo.replace(',','.'))
                producto_evento.proveedor = proveedor
                producto_evento.save()
            except:

                producto_evento = ProductoEvento.objects.create(evento=evento, producto=producto, proveedor=proveedor, precio=float(precio.replace(',','.')), precio_produccion=float(costo.replace(',','.')))
        if "combos" in request.POST:
            return HttpResponseRedirect('/listar_combos/'+id_evento+'/')
        else:
            return HttpResponseRedirect('/listar_evento/2')
    return render_to_response('evento/agregar_productos.html', {'productos': lista, 'iden': id_evento, 'proveedores': proveedores}, context_instance=RequestContext(request))

@login_required(login_url='/')
def casilla_administrativa(request, id_evento):
    evento = Evento.objects.get(id = id_evento)
    funciones = Funcion.objects.filter(evento = evento)
    staffs = AsistenciaStaffFuncion.objects.filter(funcion__in = funciones)
    if request.method == 'POST':
        posts = request.POST.items()
        for post in posts:
            aux = post[0].split("-")
            if aux[0]=="u":#------ honorarios
                if len(GastoEvento.objects.filter(evento=evento, usuario = Usuario.objects.get(id = aux[1].split(".")[0]), funcion=Funcion.objects.get(id=aux[1].split(".")[1]), nombre = Usuario.objects.get(id = aux[1].split(".")[0]).nombre+" "+Usuario.objects.get(id = aux[1].split(".")[0]).apellido+" honorarios"))>0:
                    a = GastoEvento.objects.get(evento=evento, usuario = Usuario.objects.get(id = aux[1].split(".")[0]), funcion=Funcion.objects.get(id=aux[1].split(".")[1]), nombre = Usuario.objects.get(id = aux[1].split(".")[0]).nombre+" "+Usuario.objects.get(id = aux[1].split(".")[0]).apellido+" honorarios")
                    a.monto = post[1]
                    a.save()
                else:
                    GastoEvento.objects.create(evento=evento, monto = post[1], usuario = Usuario.objects.get(id = aux[1].split(".")[0]), funcion=Funcion.objects.get(id=aux[1].split(".")[1]), nombre = Usuario.objects.get(id = aux[1].split(".")[0]).nombre+" "+Usuario.objects.get(id = aux[1].split(".")[0]).apellido+" honorarios")
            elif aux[0]=="f":#----- gastos fijos
                gastofijo =aux[1]
                if len(GastoEvento.objects.filter(evento=evento, tipo="1", nombre = gastofijo))>0:
                    a = GastoEvento.objects.get(evento=evento, tipo="1", nombre = gastofijo)
                    a.monto = post[1]
                    if len(aux)==3:
                        a.usuario = Usuario.objects.get(id=aux[2])
                    a.save()
                else:
                    if len(aux)==3:
                        GastoEvento.objects.create(evento=evento, usuario=Usuario.objects.get(id=aux[2]), monto=post[1], tipo="1", nombre = gastofijo)
                    else:
                        GastoEvento.objects.create(evento=evento, monto=post[1], tipo="1", nombre = gastofijo)
            elif aux[0]=="p":#----------porcentaje
                evento.porcentaje_institucion = post[1]
                evento.save()
            elif aux[0]=="m":#----------porcentaje(el gasto)
                if len(GastoEvento.objects.filter(evento=evento, nombre = "Porcentaje de la institcion"))>0:
                    a = GastoEvento.objects.get(evento=evento, nombre = "Porcentaje de la institcion")
                    a.monto = post[1]
                    a.save()
                else:
                    GastoEvento.objects.create(evento=evento, monto=post[1], nombre = "Porcentaje de la institcion")
            elif aux[0]=="pr":#----------Productos!
                produc = ProductoEvento.objects.get(id = aux[1])
                if len(GastoEvento.objects.filter(evento=evento, productos = produc, nombre = produc.producto.nombre))>0:
                    a = GastoEvento.objects.get(evento=evento, productos = produc, nombre = produc.producto.nombre)
                    a.monto = post[1]
                    a.save()
                else:
                    GastoEvento.objects.create(evento=evento, monto=post[1], productos = produc, nombre = produc.producto.nombre)
            elif aux[0]=="envio":#----------envios
                envio = TipoEnvio.objects.get(id = aux[1])
                if len(GastoEvento.objects.filter(evento=evento, tipo="2", nombre = envio.tipo)) > 0:
                    a = GastoEvento.objects.get(evento=evento, tipo="2", nombre = envio.tipo)
                    a.monto = float(post[1])*float(aux[1])
                    a.save()
                else:
                    GastoEvento.objects.create(evento=evento, monto=float(post[1])*float(aux[1]), tipo="2", nombre = envio)
    #---------------------------Adicionales
        if len(GastoEvento.objects.filter(evento=evento, tipo="3"))>0:
            aux = GastoEvento.objects.get(tipo="3", nombre="Cds", evento=evento)
            aux.monto = request.POST["Cds"]
            aux.save()
            aux = GastoEvento.objects.get(tipo="3", nombre="Sobres", evento=evento)
            aux.monto = request.POST["Sobres"]
            aux.save()
            aux = GastoEvento.objects.get(tipo="3", nombre="Flyers", evento=evento)
            aux.monto = request.POST["Flyers"]
            aux.save()
        else:
            GastoEvento.objects.create(nombre="Cds", monto=request.POST["Cds"], tipo="3", evento=evento)
            GastoEvento.objects.create(nombre="Sobres", monto=request.POST["Sobres"], tipo="3", evento=evento)
            GastoEvento.objects.create(nombre="Flyers", monto=request.POST["Flyers"], tipo="3", evento=evento)
    usuarios = []
    #------------------------------------------------------honorarios
    for staff in staffs:
        flag = False
        for usuario in usuarios:
            if usuario == staff.usuario:
                flag = True
        if flag == False:
            usuarios.append(staff.usuario)
    lista = []
    for usuario in usuarios:
        aux = []
        fechas = []
        for staff in staffs:
            if staff.usuario == usuario:
                bloque = StaffPorFuncion.objects.get(funcion = staff.funcion, tipo = staff.usuario.privilegio)
                gasto = GastoEvento.objects.filter(usuario=usuario, funcion=staff.funcion)
                if len(gasto) > 0:
                    gasto = gasto[0]
                    baux = Bloque(nombre=bloque.bloque.nombre, honorarios=gasto.monto, unico=bloque.bloque.unico)
                    aux.append([staff, baux])
                else:
                    if bloque.bloque.unico == True:
                        flag = False
                        for fecha in fechas:
                            if staff.funcion.dia == fecha:
                                flag = True
                        if flag == False:
                            fechas.append(staff.funcion.dia)

                            aux.append([staff, bloque.bloque])

                    else:
                        aux.append([staff, bloque.bloque])
        lista.append([usuario, aux])
    #-------------------------------------------------------Ganancias
    gananciasTotales = []
    ordenesCompras = []
    aux = []
    ProductosCombo = []
    combos = []
    ventas = 0
    combosProductoEvento = ProductoEvento.objects.filter(evento = evento, es_combo=True)
    for comboProductoEvento in combosProductoEvento:
        temp = ProductoEventoPedido.objects.filter(producto = comboProductoEvento).exclude(estado = "Creado")
        for tem in temp:
            combos.append(tem)

    for combo in combos:
        auxProductosCombo = ProductoeventoCombo.objects.filter(combo=combo.producto)
        for auxProductoCombo in auxProductosCombo:
            flag = False
            for ProductoCombo in ProductosCombo:
                if auxProductoCombo.producto.producto == ProductoCombo[0]:
                    ProductoCombo[1] = ProductoCombo[1] + (auxProductoCombo.cantidad * combo.cantidad)
                    flag = True
            if flag == False:
                ProductosCombo.append([auxProductoCombo.producto.producto, auxProductoCombo.cantidad * combo.cantidad])

    productosEvento = ProductoEvento.objects.filter(evento = evento)
    for productoEvento in productosEvento:
        aux.append(ProductoEventoPedido.objects.filter(producto = productoEvento).exclude(estado = "Creado"))
    for au in aux:
        for a in au:
            ordenesCompras.append(a)
    for ordenCompra in ordenesCompras:
        for productoEvento in productosEvento:
            if ordenCompra.producto == productoEvento:
                flag = False
                for gananciaTotales in gananciasTotales:
                    if productoEvento.producto == gananciaTotales[0]:
                        gananciaTotales[1] = gananciaTotales[1] + ordenCompra.cantidad
                        flag = True
                if flag == False:
                    gananciasTotales.append([productoEvento.producto, ordenCompra.cantidad, ordenCompra.producto.precio])

    for gananciaTotales in gananciasTotales:
        for ProductoCombo in ProductosCombo:
            if gananciaTotales[0] == ProductoCombo[0]:
                if gananciaTotales[1] - ProductoCombo[1] >= 0:
                    gananciaTotales[1] = gananciaTotales[1] - ProductoCombo[1]
                else:
                    gananciaTotales[1] = 0

    for gananciaTotales in gananciasTotales:
        ventas = ventas + (gananciaTotales[1]*gananciaTotales[2])

    #-------------------------------------------------------productos
    productosTotales = []
    ordenesCompras = []
    aux = []
    productosEvento = ProductoEvento.objects.filter(evento = evento, es_combo = False)
    for productoEvento in productosEvento:
        aux.append(ProductoEventoPedido.objects.filter(producto = productoEvento).exclude(estado = "Creado"))
    for au in aux:
        for a in au:
            ordenesCompras.append(a)
    for ordenCompra in ordenesCompras:
        for productoEvento in productosEvento:
            if ordenCompra.producto == productoEvento:
                flag = False
                for productosTotal in productosTotales:
                    if productoEvento.producto == productosTotal[0]:
                        productosTotal[1] = productosTotal[1] + ordenCompra.cantidad
                        productosTotal[2] = productosTotal[2] + productoEvento.precio_produccion*ordenCompra.cantidad
                        flag = True
                if flag == False:
                    productosTotales.append([productoEvento.producto, ordenCompra.cantidad, productoEvento.precio_produccion*ordenCompra.cantidad, ordenCompra.producto.proveedor.nombre])
    #---------combos
    temp = ProductoEvento.objects.filter(evento = evento, es_combo = True)
    auxCombos = []
    cCombos = []
    combos=[]
    for tem in temp:
        auxCombos.append(ProductoEventoPedido.objects.filter(producto = tem))
    for auxCombo in auxCombos:
        for auCombo in auxCombo:
            cCombos.append(auCombo)
    for cCombo in cCombos:
        flag = False
        for combo in combos:
            if combo[0] == cCombo.producto.producto:
                combo[1] = combo[1] + cCombo.cantidad
                flag = True
        if flag == False:
            combos.append([cCombo.producto.producto, cCombo.cantidad])

    #-------------------------------------------------------fijos
    gasto = GastoEvento.objects.filter(evento=evento, tipo=1)
    fijos = []
    if len(gasto)>0:
        for gato in gasto:
            if gato.usuario !=None :
                fijos.append([gato.nombre, gato.monto, gato.usuario.nombre+" "+gato.usuario.nombre])
            else:
                fijos.append([gato.nombre, gato.monto, ""])
    else:
        fijos = [['Viaticos', 0, ''], ['Comidas', 0, ''], ['Alquier de equipos', 0, ''], ['Deudas de staff', 0, ''], ['Edicion outsourcing', 0, '']]
    #-------------------------------------------------------envios
    numPedidos = []
    pedidos = []
    envios = []
    for ordenCompra in ordenesCompras:
        flag = False
        for numPed in numPedidos:
            if ordenCompra.num_pedido == numPed:
                flag = True
        if flag == False:
            numPedidos.append(ordenCompra.num_pedido)                   #TipoEnvio
        ordenCompra.num_pedido
    for numPed in numPedidos:
        pedidos.append(Pedido.objects.get(num_pedido=numPed).envio)
    for pedido in pedidos:
        flag = False
        for envio in envios:
            if pedido == envio[0]:
                flag = True
                envio[1] = envio[1]+1
        if flag == False:
            gasto = GastoEvento.objects.filter(evento=evento, tipo=2, nombre=pedido.tipo)
            if len(gasto)>0:
                gasto = gasto[0]
                envios.append([pedido, 1, gasto.monto])
            else:
                envios.append([pedido, 1, 0.0])
    for envio in envios:
        envio[2]=envio[2]/envio[1]
    #-------------------------------------------------------adicionales
    gasto = GastoEvento.objects.filter(evento=evento, tipo=3)
    if len(gasto)>0:
        adicionales = [GastoEvento.objects.get(evento=evento, tipo=3, nombre='Cds').monto, GastoEvento.objects.get(evento=evento, tipo=3, nombre='Sobres').monto, GastoEvento.objects.get(evento=evento, tipo=3, nombre='Flyers').monto]
    else:
        adicionales = [0, 0, 0]
    porcent = evento.porcentaje_institucion
    return render_to_response('evento/casilla_administrativa.html', {'staffs': lista, 'fijos': fijos, 'productos': productosTotales, 'envios': envios, 'porcentaje': porcent, 'adicionales': adicionales, 'ventas': ventas, 'combos': combos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def calendario_de_eventos(request):
    now = datetime.datetime.now()
    user = request.user
    usuario = Usuario.objects.get(usuario=user)
    funciones = StaffPorFuncion.objects.filter(funcion__dia__gt=now.date(), tipo=usuario.privilegio, cantidad__gt = 0).order_by('-funcion__dia').distinct()
    aux_fun = []
    for funcion in funciones:
        aux_fun.append(funcion.funcion)
    asist = AsistenciaStaffFuncion.objects.filter(usuario = usuario, funcion__in = aux_fun)
    aux_fun = []
    for funcion in funciones:
        flag = False
        for asists in asist:
            if funcion.funcion.id == asists.funcion.id:
                flag = True
        if flag == True:
            aux_fun.append([funcion, True])
        else:
            aux_fun.append([funcion, False])
    return render_to_response('evento/calendario_de_eventos.html', {'funciones': aux_fun, 'user': usuario}, context_instance=RequestContext(request))

def marcar_asistencia(request):
    if(request.GET['accion'] == 'r'):
        asistir_evento_c = AsistenciaStaffFuncion.objects.create(usuario = Usuario.objects.get(id = request.GET['userid']), funcion = Funcion.objects.get(id = request.GET['funcionid']))
    else:
        asistir_evento = AsistenciaStaffFuncion.objects.get(usuario = Usuario.objects.get(id = request.GET['userid']), funcion = Funcion.objects.get(id = request.GET['funcionid']))
        asistir_evento.delete()
    data = json.dumps({'status': "hola"})
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def usuario_por_evento(request, id_evento):
    correoForm = CorreoForm()
    even = Evento.objects.get(id = id_evento)
    funciones = Funcion.objects.filter( evento = even)
    priv = Privilegios.objects.filter( valor = 6)
    return render_to_response('evento/usuario_por_evento.html', {'funciones': funciones, 'staff':priv, 'evento': even, 'CorreoForm': correoForm}, context_instance=RequestContext(request))

def correo_staff(request):
    correoF = CorreoForm()
    evento_id = "0"
    if request.method == 'POST':
        correoF = CorreoForm(request.POST)
        if correoF.is_valid():
            evento_id = correoF.cleaned_data['evento']
            funcion = correoF.cleaned_data['funcion']
            staff = correoF.cleaned_data['staff']

            #Informacion que se extrae para el mensaje del correo
            evento = Evento.objects.get(id=evento_id)
            
            #Funcion
            funciones = Funcion.objects.filter(evento=evento)
            
            #Staff
            staffs = staff.split('.')
            tipo_staff = Privilegios.objects.get(id=staffs[0])
            
            #Correo que se enviara
            usuarios = Usuario.objects.filter(privilegio=tipo_staff)

            correos = []
            for usuario in usuarios:
                correos.append(usuario.email)

            #mensaje = 'Evento: '+str(evento.nombre)+'\nDescripcion: '+str(evento.descripcion+'\nFuncion: '+funcion.nombre+'\nTipo Staff: '+tipo_staff.nombre+'\nCantidad necesitada: '+staffs[1])
            mensaje = 'Hola!\n El presente correo es para informarte sobre el proximo evento de FOTOMOV donde nos encantaria que participaras\n\n'+str(evento.nombre)
            aux_dia = None
            for funcion in funciones:
                if aux_dia == funcion.dia:
                    pass
                else:
                    mensaje = mensaje + '\nEl ' + str(funcion.dia) + ' en ' + funcion.direccion.direccion + ':\n'
                mensaje = mensaje + '   ' + funcion.nombre + '\n'
                aux_did = funcion.dia
            mensaje = mensaje +'\n Por favor confirma tu disponibilidad ingresando con tu usuario y clave en el siguiente enlace: '
            send_mail('[FotoMov] Solicitud de staff para evento.', mensaje, '', correos, fail_silently=False)

    ctx = {}
    return HttpResponseRedirect("/usuario_por_evento/"+ str(evento_id))

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

@login_required(login_url='/')
def nuevo_tipo_de_evento(request, editado):
    tipo_eventos = Tipos_Eventos.objects.all().exclude(id=1)
    staff = Privilegios.objects.filter(valor__lt = 6)
    prelaciones = []
    if editado == '0':
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
                    TTE = TareaTipoEvento.objects.create(asignado = Privilegios.objects.get(id = staffneed), nombre = nom, tarea = desc, tipo_evento = tipoE, dias = dias, id_aux = str(tarea))
                    if prel != '0':
                        aux = str(tarea)+"-"+request.POST['prel-'+str(tarea)]
                        prelaciones.append(aux)
                for prelacion in prelaciones:
                    aux = prelacion.split('-')
                    tarea2 = TareaTipoEvento.objects.get(tipo_evento = tipoE, id_aux = aux[1])
                    tarea1 = TareaTipoEvento.objects.get(tipo_evento = tipoE, id_aux = aux[0])
                    PrelaTareaTipoEvento.objects.create(es_prelada = tarea1, prela = tarea2, tipo_evento=tipoE)
                return HttpResponseRedirect('/nuevo_tipo_de_evento/0/')
        else:
            formulario = TiposEventoForm()
    else:
        tEvento = Tipos_Eventos.objects.get(id = editado)
        tareas = TareaTipoEvento.objects.filter(tipo_evento = tEvento)
        Pprelaciones = PrelaTareaTipoEvento.objects.filter(tipo_evento = Tipos_Eventos.objects.get(id = editado))
        if(request.method == 'POST'):
            formulario = TiposEventoForm(request.POST)
            if(formulario.is_valid()):
                for prelacion in prelaciones:
                    prelacion.delete()
                for tarea in tareas:
                    tarea.delete()
                tEvento.nombre = request.POST['nombre']
                tEvento.save()
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
                    TTE = TareaTipoEvento.objects.create(asignado = Privilegios.objects.get(id = staffneed), nombre = nom, tarea = desc, tipo_evento = tEvento, dias = dias, id_aux = str(tarea))
                    if prel != '0':
                        aux = str(tarea)+"-"+request.POST['prel-'+str(tarea)]
                        prelaciones.append(aux)
                for prelacion in prelaciones:
                    aux = prelacion.split('-')
                    tarea2 = TareaTipoEvento.objects.get(tipo_evento = tEvento, id_aux = aux[1])
                    tarea1 = TareaTipoEvento.objects.get(tipo_evento = tEvento, id_aux = aux[0])
                    PrelaTareaTipoEvento.objects.create(es_prelada = tarea1, prela = tarea2, tipo_evento=tEvento)
                return HttpResponseRedirect('/nuevo_tipo_de_evento/0/')
        else:
            formulario = TiposEventoForm(initial={"nombre": tEvento.nombre})
        return render_to_response('evento/nuevo_tipo_de_evento.html', {'formulario': formulario, 'eventos': tipo_eventos, 'staff': staff, 'editado': editado, 'tipoEvento': tEvento, 'tareas': tareas, 'prelaciones': Pprelaciones}, context_instance=RequestContext(request))
    return render_to_response('evento/nuevo_tipo_de_evento.html', {'formulario': formulario, 'eventos': tipo_eventos, 'staff': staff, 'editado': editado}, context_instance=RequestContext(request))

@login_required(login_url='/')
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

@login_required(login_url='/')
def listar_pautas(request, id_evento, creado):
    evento = Evento.objects.get(id=id_evento)
    pautas = Pautas.objects.filter(evento=evento)
    return render_to_response('evento/listar_pautas.html', {'pautas': pautas, 'evento': evento, 'creado': creado}, context_instance=RequestContext(request))

@login_required(login_url='/')
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

@login_required(login_url='/')
def eliminar_pauta(request, id_pauta):
    pauta = Pautas.objects.get(id=id_pauta)
    id_evento = pauta.evento.id
    pauta.delete()
    return HttpResponseRedirect("/listar_pautas/" + str(id_evento) + "/3")

@login_required(login_url='/')
def ver_pauta(request, id_pauta):
    pauta = Pautas.objects.get(id=id_pauta)
    return render_to_response('evento/ver_pauta.html', {'pauta': pauta}, context_instance=RequestContext(request))

@login_required(login_url='/')
def crear_bloque(request):
    if request.method == 'POST':
        formulario = BloqueForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listar_bloques/0/')
    else:
        formulario = BloqueForm()
    return render_to_response('evento/crear_bloque.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_bloques(request, id_bloque):
    if id_bloque != '0':
        bloque = Bloque.objects.filter(id = id_bloque)
        if len(bloque)!=0:
            bloque = bloque[0]
            bloque.delete()
    bloques = Bloque.objects.all()
    return render_to_response('evento/listar_bloques.html', {'bloques': bloques}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_bloque(request, id_bloque):
    bloque = Bloque.objects.get(id = id_bloque)
    if request.method == 'POST':
        formulario = BloqueForm(request.POST)
        if formulario.is_valid():
            bloque.nombre = formulario.cleaned_data['nombre']
            bloque.honorarios = formulario.cleaned_data['honorarios']
            bloque.unico = formulario.cleaned_data['unico']
            bloque.save()
            bloques = Bloque.objects.all()
            return render_to_response('evento/listar_bloques.html', {'bloques': bloques}, context_instance=RequestContext(request))
    else:
        formulario = BloqueForm(initial = {'nombre':bloque.nombre, 'honorarios':bloque.honorarios, 'unico':bloque.unico})
    return render_to_response('evento/editar_bloque.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_evento(request, iden):
    evento = Evento.objects.get(id = iden)
    funciones = Funcion.objects.filter(evento = evento)
    gastos_predeterminados = Gasto.objects.filter(predeterminado = True)
    direcciones = obtener_direcciones()
    if request.method == 'POST':
        formulario = EventoForm(request.POST)
        if formulario.is_valid():
            if evento.macrocliente != None:
                encargado = Encargado.objects.get(id=request.POST.get('encargado'))
                sede = Sede.objects.get(id=request.POST.get('sede'))
                evento.encargado = encargado
                evento.sede = sede
                evento.macrocliente = formulario.cleaned_data['macrocliente']
                evento.submarca = evento.macrocliente.submarca
            else:
                evento.cliente = Cliente.objects.get(cedula=request.POST.get('cliente').split('-')[1])
                print request.POST.get('submarca')
                evento.submarca = SubMarca.objects.get(id=request.POST.get('submarca'))
            evento.nombre = formulario.cleaned_data['nombre']
            evento.descripcion = formulario.cleaned_data['descripcion']
            evento.porcentaje_institucion = formulario.cleaned_data['porcentaje_institucion']
            evento.fecha_entrega = formulario.cleaned_data['fecha_entrega']
            evento.tipo = formulario.cleaned_data['tipo']
            evento.save()
            return HttpResponseRedirect('/listar_evento/2/')
    else:
        if evento.macrocliente != None:
            formulario = EventoForm(initial={'nombre': evento.nombre, 'descripcion': evento.descripcion,
                                             'macrocliente': evento.macrocliente, 'tipo': evento.tipo, 'fecha_entrega':evento.fecha_entrega})
        else:
            formulario = EventoForm(initial={'nombre': evento.nombre, 'descripcion': evento.descripcion,
                                             'marcas': evento.submarca.marca, 'tipo': evento.tipo, 'fecha_entrega':evento.fecha_entrega})
    return render_to_response('evento/editar_evento.html', {'evento': evento, 'funciones': funciones, 'formulario': formulario, 'gastos': gastos_predeterminados, 'direcciones': direcciones}, context_instance=RequestContext(request))


def editar_funcion(request):
    print "entre"
    if request.GET['accion']=='1':#actualizar
        funcion = Funcion.objects.get(id = request.GET['iden'])
        funcion.nombre = request.GET['nomb']
        funcion.horas = request.GET['horas']
        if request.GET['dia'] != '':
            #fecha = datetime.datetime.strptime(request.GET['dia'], "%m/%d/%Y")
            #print fecha
            dia_split = request.GET['dia'].split('/')
            dia_final = dia_split[2] + "-" + dia_split[0] + "-" + dia_split[1]
            print dia_split
            print dia_final
            funcion.dia = dia_final
        funcion.save()
        try:
            direccionFuncion.objects.get(funcion=funcion).delete()
            if funcion.evento.macrocliente != None:
                directorio = direccionFuncion.objects.create(funcion=funcion, dir = funcion.evento.macrocliente.submarca.marca.nombre + "/" + funcion.evento.macrocliente.submarca.nombre + "/" + funcion.evento.macrocliente.nombre + "/" + funcion.evento.nombre + "/" + funcion.evento.sede.nombre + "/" + funcion.dia + "/" + funcion.direccion.nombre + "/" +funcion.nombre)
        except:
            if funcion.evento.macrocliente != None:
                directorio = direccionFuncion.objects.create(funcion=funcion, dir = funcion.evento.macrocliente.submarca.marca.nombre + "/" + funcion.evento.macrocliente.submarca.nombre + "/" + funcion.evento.macrocliente.nombre + "/" + funcion.evento.nombre + "/" + funcion.evento.sede.nombre + "/" + funcion.dia + "/" + funcion.direccion.nombre + "/" +funcion.nombre)
        #directorio = direccionFuncion.objects.create(funcion=funcion, dir = funcion.evento.macrocliente.submarca.marca.nombre + "/" + funcion.evento.macrocliente.submarca.nombre + "/" + funcion.evento.macrocliente.nombre + "/" + funcion.evento.nombre + "/" + funcion.evento.sede.nombre + "/" + funcion.dia + "/" + funcion.direccion.nombre + "/" +funcion.nombre)
    elif request.GET['accion']=='2':#agregar
        evento = Evento.objects.get(id = request.GET['evento'])
        dia_split = request.GET['dia'].split('/')
        dia_final = dia_split[2] + "-" + dia_split[0] + "-" + dia_split[1]
        funcion = Funcion.objects.create(nombre = request.GET['nomb'], evento = evento, dia = dia_final, horas = request.GET['horas'], entrega_fotos = '', direccion = Direccion.objects.get(id=1))
        if funcion.evento.macrocliente != None:
            directorio = direccionFuncion.objects.create(funcion=funcion, dir = funcion.evento.macrocliente.submarca.marca.nombre + "/" + funcion.evento.macrocliente.submarca.nombre + "/" + funcion.evento.macrocliente.nombre + "/" + funcion.evento.nombre + "/" + funcion.evento.sede.nombre + "/" + funcion.dia + "/" + funcion.direccion.nombre + "/" +funcion.nombre)
    elif request.GET['accion']=='3':#borrar
        funcion = Funcion.objects.get(id = request.GET['iden'])
        direccionFuncion.objects.get(funcion=funcion).delete()
        funcion.delete()
    elif request.GET['accion']=='4':#locacion
        loc = Direccion.objects.filter(nombre = request.GET['nomb'])
        funcion = Funcion.objects.get(id = request.GET['iden'])
        if len(loc) > 0:
            loc = loc[0]
        funcion.direccion = loc;
        funcion.save()
        nomb = loc.nombre
        data = json.dumps({'nombre':nomb})
        return HttpResponse(data, mimetype='application/json')
    data = json.dumps({'id':funcion.id, 'nombre':funcion.nombre , 'evento':funcion.evento.nombre, 'horas':funcion.horas, 'entrega_fotos':funcion.entrega_fotos, 'dia': str(funcion.dia), 'direccion':funcion.direccion.nombre, 'accion': request.GET['accion']})
    return HttpResponse(data, mimetype='application/json')

def traer_usuario_gasto_evento_ajax(request):
    usuarioN = Usuario.objects.filter(nombre__contains = request.GET['usu'])
    usuarioA = Usuario.objects.filter(apellido__contains = request.GET['usu'])
    usuarioC = Usuario.objects.filter(cedula__contains = request.GET['usu'])

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
        resp.append({"value": usuario.id, "label": usuario.nombre+" "+usuario.apellido, "desc": usuario.privilegio.nombre+" - "+usuario.cedula})

    print resp

    return HttpResponse(simplejson.dumps(resp), mimetype='application/json')

@login_required(login_url='/')
def crear_combos(request, evento_id):
    productos = ProductoEvento.objects.filter(evento = Evento.objects.get(id = evento_id), es_combo=False)
    if request.method == 'POST':
        if request.POST['nombre'] != '' and request.POST['precio'] != '' and int(request.POST['numprop']) > 0:
            combop = Producto.objects.create(nombre = request.POST['nombre'], descripcion = request.POST['desc'], es_combo=True)
            combo = ProductoEvento(producto = combop, precio = request.POST['precio'], evento=Evento.objects.get(id=evento_id), es_combo=True)
            produccion = 0
            for i in range(int(request.POST['numprop'])):
                aux = request.POST['check-'+str(i)].split("-")
                iden = aux[0]
                cant = aux[1]
                produccion = produccion + (float(ProductoEvento.objects.get(id=iden).precio_produccion) * float(cant))
            combo.precio_produccion = produccion
            combo.save()
            for i in range(int(request.POST['numprop'])):
                aux = request.POST['check-'+str(i)].split("-")
                iden = aux[0]
                cant = aux[1]
                ProductoeventoCombo.objects.create(producto=ProductoEvento.objects.get(id=iden), combo=combo, cantidad=cant)
            return HttpResponseRedirect('/listar_combos/'+evento_id+'/')
        else:
            messages.add_message(request, messages.ERROR, 'Debe llenar todos los campos', extra_tags='danger')
    return render_to_response('evento/crear_combos.html', {'iden': evento_id, 'productos': productos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_combos(request, evento_id):
    combos = ProductoEvento.objects.filter(evento=Evento.objects.get(id=evento_id), es_combo = True)
    return render_to_response('evento/listar_combos.html', {'iden': evento_id, 'combos': combos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_combo(request, combo_id):
    combo = ProductoEvento.objects.get(id = combo_id)
    productos = ProductoeventoCombo.objects.filter(combo = combo)
    iden = combo.evento.id
    return render_to_response('evento/ver_combo.html', {'iden': iden, 'combo': combo, 'productos': productos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_combo(request, combo_id):
    combo = ProductoEvento.objects.get(id = combo_id)
    productos = ProductoeventoCombo.objects.filter(combo = combo)
    for producto in productos:
        producto.delete()
    iden = combo.evento.id
    combo.delete()
    return HttpResponseRedirect('/listar_combos/'+str(iden)+'/')

@login_required(login_url='/')
def editar_combo(request, combo_id):
    combo = ProductoEvento.objects.get(id = combo_id)
    iden = combo.evento.id
    productos = ProductoEvento.objects.filter(evento=combo.evento, es_combo=False)
    productosCombos = ProductoeventoCombo.objects.filter(combo=combo)
    for p in productosCombos:
        print p.id
    if request.method == 'POST':
        if request.POST['nombre'] != '' and request.POST['precio'] != '' and int(request.POST['numprop']) > 0:
            combop = combo.producto
            combop.nombre = request.POST['nombre']
            combop.descripcion = request.POST['desc']
            combop.es_combo=True
            combop.save()

            combo.producto = combop
            combo.precio = request.POST['precio']
            combo.es_combo=True

            produccion = 0
            for i in range(int(request.POST['numprop'])):
                aux = request.POST['check-'+str(i)].split("-")
                iden = aux[0]
                cant = aux[1]
                produccion = produccion + (float(ProductoEvento.objects.get(id=iden).precio_produccion) * float(cant))
            combo.precio_produccion = produccion
            combo.save()

            ps = ProductoeventoCombo.objects.filter(combo = combo)
            for p in ps:
                p.delete()

            for i in range(int(request.POST['numprop'])):
                aux = request.POST['check-'+str(i)].split("-")
                iden = aux[0]
                cant = aux[1]
                ProductoeventoCombo.objects.create(producto=ProductoEvento.objects.get(id=iden), combo=combo, cantidad=cant)
            return HttpResponseRedirect('/listar_combos/'+str(combo.evento.id)+'/')
    return render_to_response('evento/editar_combo.html', {'iden': iden, 'combo': combo, 'productos': productos, 'productosC': productosCombos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_tipo_evento(request, tipo_id):
    tipoEvento = Tipos_Eventos.objects.get(id= tipo_id)
    tareas = TareaTipoEvento.objects.filter(tipo_evento = tipoEvento)
    prelaciones = PrelaTareaTipoEvento.objects.filter(tipo_evento = tipoEvento)
    for prelacion in prelaciones:
        prelacion.delete()
    for tarea in tareas:
        tarea.delete()
    tipoEvento.delete()
    return HttpResponseRedirect("/nuevo_tipo_de_evento/0/")

@login_required(login_url='/')
def ver_tipo_evento(request, tipo_id):
    tipoEvento = Tipos_Eventos.objects.get(id= tipo_id)
    tareas = TareaTipoEvento.objects.filter(tipo_evento = tipoEvento)
    Pprelaciones = PrelaTareaTipoEvento.objects.filter(tipo_evento = tipoEvento)
    return render_to_response('evento/ver_tipo_evento.html', {'tipoe': tipoEvento, 'tareas': tareas, 'prelaciones': Pprelaciones}, context_instance=RequestContext(request))

@login_required(login_url='/')
def nuevo_item(request):
    if request.method == 'POST':
        formulario = NuevoItemForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listar_items/1')
    else:
        formulario = NuevoItemForm()
    return render_to_response('evento/nuevo_item.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_item(request, id_item):
    item = Items.objects.get(id=id_item)
    if request.method == 'POST':
        formulario = NuevoItemForm(request.POST)
        if formulario.is_valid():
            form = formulario.save(commit=False)
            item.item = form.item
            item.cantidad = form.cantidad
            item.save()
            return HttpResponseRedirect('/listar_items/2')
    else:
        formulario = NuevoItemForm(instance=item)
    return render_to_response('evento/nuevo_item.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_items(request, id_item):
    item = Items.objects.get(id=id_item)
    item.delete()
    return HttpResponseRedirect('/listar_items/3')

@login_required(login_url='/')
def listar_items(request, creado):
    items = Items.objects.all()

    return render_to_response('evento/listar_items.html', {'items': items, 'creado': creado}, context_instance=RequestContext(request))

@login_required(login_url='/')
def asignar_item_staff(request, id_evento):
    evento = Evento.objects.get(id=id_evento)
    return render_to_response('evento/asignar_item_staff.html', {'evento': evento}, context_instance=RequestContext(request))


def enviar_correo_convocados(request):
    evento=Evento.objects.get(id = request.GET['evento'])
    funciones = Funcion.objects.filter(evento = evento)
    aux=[]
    usuarios=[]
    for funcion in funciones:
        aux.append(AsistenciaStaffFuncion.objects.filter(funcion= funcion, fue_convocado=True))
    for au in aux:
        for a in au:
            usuarios.append(a.usuario)
    correos = []
    for usuario in usuarios:
        correos.append(usuario.email)
    mensaje = request.GET['mail']
    if mensaje != '':
        send_mail('[FotoMov] Convocatoria de staff para evento.', mensaje, '', correos, fail_silently=False)
    data = json.dumps({'nombre': ''})
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/')
def listar_items_prestados(request, id_evento):
    evento = Evento.objects.get(id = id_evento)
    items = ItemsPrestado.objects.filter(evento = evento).order_by('-devuelto')
    return render_to_response('evento/listar_items_prestados.html', {'items': items, 'evento': id_evento}, context_instance=RequestContext(request))


@login_required(login_url='/')
def devolver_item_ajax(request):
    item = ItemsPrestado.objects.get(id=request.GET['iden'])
    item.devuelto = True
    item.estado = request.GET['estado']
    item.save()
    data = json.dumps({'nombre': ''})
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/')
def prestar_item_seleccionado(request):
    item = Items.objects.get(id=request.GET['iden'])
    nombres = request.GET['per']
    nombres = nombres.split()
    usuario = Usuario.objects.get(nombre=nombres[0], apellido=nombres[1])
    evento = Evento.objects.get(id=request.GET['evento'])
    ItemsPrestado.objects.create(item=item, usuario=usuario, evento=evento)
    data = json.dumps({'nombre': ''})
    return HttpResponse(data, mimetype='application/json')


@login_required(login_url='/')
def eliminar_prestamo(request, id_prestamo):
    item = ItemsPrestado.objects.get(id = id_prestamo)
    evento = item.evento
    item.delete()
    return HttpResponseRedirect('/listar_items_presatdos/'+str(evento.id)+'/')


@login_required(login_url='/')
def prestar_item(request, id_evento):
    items = Items.objects.all()
    return render_to_response('evento/prestar_item.html', {'items': items, 'evento': id_evento}, context_instance=RequestContext(request))

@login_required(login_url='/')
def calendario_entregas(request):
    if datetime.datetime.today().month == 1:
        hoy = date(datetime.datetime.today().year, 12, datetime.datetime.today().day)
    else:
        hoy = date(datetime.datetime.today().year, datetime.datetime.today().month-1, datetime.datetime.today().day)
    eventos = Evento.objects.filter(fecha_entrega__gte = hoy)
    return render_to_response('evento/calendario_entregas.html', {'eventos': eventos}, context_instance=RequestContext(request))
