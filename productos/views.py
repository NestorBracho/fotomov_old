import json
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.models import modelform_factory
from productos.models import *
from productos.forms import *
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.core.mail import send_mail
import datetime

@login_required(login_url='/')
def nuevo_producto(request):
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()
            if "agregar" in request.POST:
                return HttpResponseRedirect('/listar_producto/1')
            else:
                messages.add_message(request, messages.SUCCESS, 'El producto se ha agregado exitosamente.', extra_tags='success')
                return HttpResponseRedirect('/nuevo_producto/')
    else:
        formulario = ProductoForm()
    return render_to_response('productos/nuevo_producto.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_producto(request, creado):
    productos = Producto.objects.filter(es_combo=False)
    return render_to_response('productos/listar_producto.html', {'productos': productos, "creado": creado}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_producto(request, id_producto):
    producto = Producto.objects.get(id=id_producto)
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            editado = formulario.save(commit=False)
            producto.nombre = editado.nombre
            producto.descripcion = editado.descripcion
            producto.save()
            return HttpResponseRedirect('/listar_producto/2')
    else:
        formulario = ProductoForm(initial={'nombre': producto.nombre, 'descripcion': producto.descripcion})
    return render_to_response('productos/nuevo_producto.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_producto(request, id_producto):
    producto = Producto.objects.get(id=id_producto).delete()
    return HttpResponseRedirect('/listar_producto/3')

@login_required(login_url='/')
def edicion_lotes(request):
    lotes_edicion = Lote.objects.filter(estado = 'Edicion')
    lotes_listos = Lote.objects.filter(estado = 'Editado')

    pedidos = []
    for lote_edicion in lotes_edicion:
        pedido = [lote_edicion.codigo,0,0,lote_edicion.id]
        pedidos_en_lote = Pedido.objects.filter(lote = lote_edicion)
        for pedido_en_lote in pedidos_en_lote:
            if pedido_en_lote.estado == 'Editado':
                pedido[1] = pedido[1] + 1
            pedido[2] = pedido[2] + 1
        pedidos.append(pedido)

    listos = []
    for lote_listo in lotes_listos:
        listo = [lote_listo.codigo,0,0,lote_listo.id]
        pedidos_en_lote = Pedido.objects.filter(lote = lote_listo)
        for pedido_en_lote in pedidos_en_lote:
            if pedido_en_lote.estado == 'Editado':
                listo[1] = listo[1]+1
            listo[2] = listo[2]+1
        listos.append(listo)
    return render_to_response('productos/edicion_lotes.html', {'edicion': pedidos, 'listos': listos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def edicion_productos(request, pedido):
    pedidos_edicion = ProductoEventoPedido.objects.filter(num_pedido=Pedido.objects.get(id=pedido).num_pedido, estado='Edicion')
    pedidos_editados = ProductoEventoPedido.objects.filter(Q(num_pedido=Pedido.objects.get(id=pedido).num_pedido, estado='Editado') | Q(num_pedido=Pedido.objects.get(id=pedido).num_pedido, estado='Vale por foto'))
    return render_to_response('productos/edicion_productos.html', {'edicion': pedidos_edicion, 'editados': pedidos_editados, 'pedido': Pedido.objects.get(id=pedido)}, context_instance=RequestContext(request))


def cambiar_estado_producto_edicion(request):
    producto = ProductoEventoPedido.objects.get(id = request.GET['iden'])
    pedido = Pedido.objects.get(num_pedido=producto.num_pedido)
    if producto.estado == 'Edicion':
        producto.estado = request.GET['estado']
        producto.save()
        tProductos = ProductoEventoPedido.objects.filter(num_pedido = producto.num_pedido)
        parcial = 0
        total = 0
        for tProducto in tProductos:
            total = total + 1
            if tProducto.estado == 'Editado' or tProducto.estado == 'Vale por foto':
                parcial = parcial + 1
        if parcial == total:

            pedido.estado = "Editado"
            pedido.save()
        parcial = 0
        total = 0
        tPedidos = Pedido.objects.filter(lote = pedido.lote)
        aux = []
        aux2 = []
        for tPedido in tPedidos:
            aux.append(ProductoEventoPedido.objects.filter(num_pedido = tPedido.num_pedido))
        for a in aux:
            for au in a:
                aux2.append(au)
        tProductos = aux2
        for tProducto in tProductos:
            total = total + 1
            if tProducto.estado == 'Editado' or tProducto.estado == 'Vale por foto':
                parcial = parcial + 1
        if parcial == total:
            pedido.lote.estado = "Editado"
            pedido.lote.save()
    else:
        pedido = Pedido.objects.get(num_pedido=producto.num_pedido)
        pedido.lote.estado = 'Edicion'
        pedido.lote.save()
        pedido.estado = 'Edicion'
        pedido.save()
        producto.estado = 'Edicion'
        producto.save()
    data = json.dumps({'estado': producto.estado})
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def edicion_pedido(request, lote):
    pedidos_edicion = Pedido.objects.filter(lote = Lote.objects.get(id = lote), estado = 'Edicion')
    pedidos_listos = Pedido.objects.filter(lote = Lote.objects.get(id = lote), estado = 'Editado')
    pedidos = []
    for pedido_edicion in pedidos_edicion:
        pedido = [pedido_edicion.num_pedido,0,0,pedido_edicion.id]
        productos_en_pedido = ProductoEventoPedido.objects.filter(num_pedido = pedido_edicion.num_pedido)
        for producto_en_pedido in productos_en_pedido:
            if producto_en_pedido.estado == 'Editado':
                pedido[1] = pedido[1] + 1
            pedido[2] = pedido[2] + 1
        pedidos.append(pedido)

    listos = []
    for pedido_listo in pedidos_listos:
        listo = [pedido_listo.num_pedido,0,0,pedido_listo.id]
        productos_en_pedido = ProductoEventoPedido.objects.filter(num_pedido = pedido_listo.num_pedido)
        for producto_en_pedido in productos_en_pedido:
            if producto_en_pedido.estado == 'Editado':
                listo[1] = listo[1]+1
            listo[2] = listo[2]+1
        listos.append(listo)
    return render_to_response('productos/edicion_pedidos.html', {'edicion': pedidos, 'listos':listos, 'lote': Lote.objects.get(id = lote)}, context_instance=RequestContext(request))

@login_required(login_url='/')
def administrar_lotes(request):
    lotes = Lote.objects.all()
    return render_to_response('productos/administrar_lotes.html', {'lotes':lotes}, context_instance=RequestContext(request))

@login_required(login_url='/')
def administrar_pedidos(request, lote):
    lote = Lote.objects.get( id = lote)
    pedidos = Pedido.objects.filter(lote = lote)
    return render_to_response('productos/administrar_pedidos.html', {'pedidos':pedidos, 'lote':lote}, context_instance=RequestContext(request))

def cambiar_estado_lotes_desde_administrar_pedidos(request):
    lote = Lote.objects.get(id = request.GET['lote'])
    pedidos = Pedido.objects.filter(lote = lote)
    productos = []
    productosA = []
    boton_estado = ''
    for pedido in pedidos:
        productosA.append(ProductoEventoPedido.objects.filter(num_pedido = pedido.num_pedido))
    for PAU in productosA:
        for PA in PAU:
            productos.append(PA)

    if lote.estado == 'Edicion':
        lote.estado = 'Editado'
        boton_estado = 'Impresion'
    elif lote.estado == 'Editado':
        lote.estado = 'Impresion'
        boton_estado = 'Impreso'
    elif lote.estado == 'Impresion':
        lote.estado = 'Impreso'
        boton_estado = 'Listo'
    elif lote.estado == 'Impreso':
        lote.estado = 'Listo'
        boton_estado = 'Done'
    lote.save()

    for pedido in pedidos:
        pedido.estado = lote.estado
        pedido.save()
    for producto in productos:
        producto.estado = lote.estado
        producto.save()

    data = json.dumps({'boton': boton_estado, 'estado': lote.estado})
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render_to_response('productos/listar_pedidos.html', {'pedidos':pedidos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_pedido(request, pedido):
    pedido = Pedido.objects.get(id = pedido)
    productos = ProductoEventoPedido.objects.filter(num_pedido = pedido.num_pedido)
    return render_to_response('productos/ver_pedido.html', {'pedido': pedido, 'productos': productos}, context_instance=RequestContext(request))

def verpedido_cambiar_estado_pedido_p_np(request):
    pedido = Pedido.objects.get(id = request.GET['iden'])
    if pedido.fue_pagado == True:
        pedido.fue_pagado = False
    else:
        pedido.fue_pagado = True
    pedido.save()
    data = json.dumps({'estado': pedido.fue_pagado})
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def listar_pedidos_pendientes(request):
    pedidos = Pedido.objects.filter(fue_pagado = False)
    return render_to_response('productos/listar_pedidos_pendiente.html', {'pedidos':pedidos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_pedidos_sin_pagar(request):
    pedidos = Pedido.objects.filter(fue_pagado=False)
    return render_to_response('productos/listar_pedidos_sin_pagar.html', {'pedidos':pedidos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_facturas_pendientes(request):
    pedidos=Pedido.objects.filter(fue_pagado=True, factura=False)
    return render_to_response('productos/listar_facturas_pendientes.html', {'pedidos':pedidos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_facturas_todas(request):
    pedidos=Pedido.objects.filter(fue_pagado=True)
    return render_to_response('productos/listar_facturas_pendientes.html', {'pedidos':pedidos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def descargar_factura(request, id_factura):
    # Create the HttpResponse object with the appropriate PDF headers.
    pedido = Pedido.objects.get(id=id_factura)
    factura = "factura-" + pedido.cliente.nombres + "-" + pedido.cliente.apellidos + ".pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + factura + ''
    p = canvas.Canvas(response)
    fecha_aux = str(datetime.datetime.now()).split(" ")
    fecha = fecha_aux[0]
    productos = ProductoEventoPedido.objects.filter(num_pedido=pedido.num_pedido)
    subtotal = 0
    y = 650
    for producto in productos:
        cant = str(producto.cantidad)
        descripcion = str(producto.producto.producto.nombre)
        precio = str(producto.producto.precio)
        monto = str(producto.producto.precio * producto.cantidad)
        p.drawString(100,y,cant)
        p.drawString(240,y,descripcion)
        p.drawString(380,y, precio)
        p.drawString(520,y,monto)
        subtotal = subtotal + float(monto)
        print subtotal
        y = y - 15
    p.drawString(100,730,pedido.razon_social)
    lista_dir_fiscal = pedido.direccion_fiscal.split(" ")
    dir_ini = " ".join(lista_dir_fiscal[:len(lista_dir_fiscal)/2])
    dir_final = " ".join(lista_dir_fiscal[len(lista_dir_fiscal)/2:])
    print lista_dir_fiscal[len(lista_dir_fiscal)/2]
    p.drawString(100,715,dir_ini)
    p.drawString(100,700,dir_final)
    p.drawString(400,730,str(fecha))
    p.drawString(400,715,pedido.id_fiscal)
    p.drawString(400,700,pedido.tlf_fiscal)
    p.drawString(400,500, str(subtotal))
    iva = float(subtotal)*0.12
    p.drawString(400,485, str(iva))
    total = subtotal + iva
    p.drawString(400,470, str(total))
    p.showPage()
    p.save()
    pedido.factura=True
    pedido.save()
    return response

def editar_productoeventopedido_en_generarpedido(request):
    #'iden': iden, 'cantidad': cantidad, 'precio': precio, 'estado': estado
    pedido = ProductoEventoPedido.objects.get(id = request.GET['iden'])
    if request.GET['task'] == '1':#cargar
        data = json.dumps({'comentario': pedido.comentario})
        return HttpResponse(data, mimetype='application/json')
    elif request.GET['task'] == '2':#modificar
        macropedido = Pedido.objects.get(num_pedido = pedido.num_pedido)
        todosLosPedidos = ProductoEventoPedido.objects.filter(num_pedido = pedido.num_pedido)
        pedido.cantidad = request.GET['cantidad']
        pedido.estado = request.GET['estado']
        pedido.comentario = request.GET['comentario']
        pedido.save()
        total = 0
        for LosPedidos in todosLosPedidos:
            total = total + (LosPedidos.cantidad*LosPedidos.producto.precio)
        macropedido.total = total
        macropedido.save()
        data = json.dumps({'total': macropedido.total})
        return HttpResponse(data, mimetype='application/json')
    elif request.GET['task'] == '3':#Eliminar
        macropedido = Pedido.objects.get(num_pedido = pedido.num_pedido)
        todosLosPedidos = ProductoEventoPedido.objects.filter(num_pedido = pedido.num_pedido)
        pedido.delete()
        total = 0
        for LosPedidos in todosLosPedidos:
            total = total + (LosPedidos.cantidad*LosPedidos.producto.precio)
        macropedido.total = total
        macropedido.save()
    data = json.dumps({'estado': 'hola'})
    return HttpResponse(data, mimetype='application/json')

@login_required(login_url='/')
def crear_proveedor(request):
    if request.method == 'POST':
        formulario = ProveedorForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()
            return HttpResponseRedirect('/listar_proveedores/')
    else:
        formulario = ProveedorForm()
    return render_to_response('productos/crear_proveedor.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render_to_response('productos/listar_proveedores.html', {'proveedores': proveedores}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_proveedor(request, id_proveedor):
    proveedor = Proveedor.objects.get(id = id_proveedor)
    return render_to_response('productos/ver_proveedor.html', {'proveedor': proveedor}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_proveedor(request, id_proveedor):
    proveedor = Proveedor.objects.get(id = id_proveedor)
    proveedor.delete()
    return HttpResponseRedirect('/listar_proveedores/')

@login_required(login_url='/')
def editar_proveedor(request, id_proveedor):
    proveedor = Proveedor.objects.get(id = id_proveedor)
    if request.method == 'POST':
        formulario = ProveedorForm(request.POST, instance = proveedor)
        if formulario.is_valid():
            producto = formulario.save()
            return HttpResponseRedirect('/listar_proveedores/')
    else:
        formulario = ProveedorForm(instance = proveedor)
    return render_to_response('productos/editar_proveedor.html', {'formulario': formulario}, context_instance=RequestContext(request))


@login_required(login_url='/')
def listar_envios(request):
    if request.method == 'POST':
        ped = Pedido.objects.get(num_pedido=request.POST["num_pedido"])
        EnvioPedido.objects.create(pedido=ped, tracking=request.POST["tracking"], proveedor=request.POST["proveedor"])
    temp = TipoEnvio.objects.filter(req_dir=True).values_list('id', flat=True)
    pedidos = Pedido.objects.filter(envio__in=temp)
    envios = EnvioPedido.objects.filter(pedido__in=pedidos.values_list('id', flat=True))
    return render_to_response('productos/listar_envios.html', {'envios': envios, 'pedidos': pedidos}, context_instance = RequestContext(request))

def enviar_mail_de_estado(request):
    pedidos = Pedido.objects.filter(lote = Lote.objects.get(id = request.GET['lote']))
    correos = []
    for pedido in pedidos:
        correos.append(pedido.cliente.email)
    mensaje = request.GET['mensaje']
    send_mail('[FotoMov] Estado de su pedido.', mensaje, '', correos, fail_silently=False)

    data = json.dumps({'estado': 'hola'})
    return HttpResponse(data, mimetype='application/json')

def enviar_mail_de_tracking_de_envio(request):
    pedidos = Pedido.objects.get(id = request.GET['pedido'])
    #correos = []
    correos = [pedidos.cliente.email]
    mensaje = request.GET['mensaje']
    send_mail('[FotoMov] Tracking de su pedido.', mensaje, '', correos, fail_silently=False)

    data = json.dumps({'estado': 'hola'})
    return HttpResponse(data, mimetype='application/json')