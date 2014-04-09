import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from productos.models import *
from productos.forms import *

def nuevo_producto(request):
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()
            return HttpResponseRedirect('/listar_producto/1')
    else:
        formulario = ProductoForm()
    return render_to_response('productos/nuevo_producto.html', {'formulario': formulario}, context_instance=RequestContext(request))

def listar_producto(request, creado):
    productos = Producto.objects.all()
    return render_to_response('productos/listar_producto.html', {'productos': productos, "creado": creado}, context_instance=RequestContext(request))

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

def eliminar_producto(request, id_producto):
    producto = Producto.objects.get(id=id_producto).delete()
    return HttpResponseRedirect('/listar_producto/3')

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

def edicion_productos(request, pedido):
    pedidos_edicion = ProductoEventoPedido.objects.filter(pedido = Pedido.objects.get(id = pedido), estado = 'Edicion')
    pedidos_editados = ProductoEventoPedido.objects.filter(pedido = Pedido.objects.get(id = pedido), estado = 'Editado')
    return render_to_response('productos/edicion_productos.html', {'edicion': pedidos_edicion, 'editados': pedidos_editados, 'pedido': Pedido.objects.get(id = pedido)}, context_instance=RequestContext(request))

def cambiar_estado_producto_edicion_a_editado(request):
    producto = ProductoEventoPedido.objects.get(id = request.GET['iden'])
    producto.estado = 'Editado'
    producto.save()
    tProductos = ProductoEventoPedido.objects.filter(pedido = producto.pedido)
    parcial = 0
    total = 0
    for tProducto in tProductos:
        total = total + 1
        if tProducto.estado == 'Editado':
            parcial = parcial + 1
    if parcial == total:
        producto.pedido.estado = "Editado"
        producto.pedido.save()
    parcial = 0
    total = 0
    tPedidos = Pedido.objects.filter(lote = producto.pedido.lote)
    aux = []
    aux2 = []
    for tPedido in tPedidos:
        aux.append(ProductoEventoPedido.objects.filter(pedido = tPedido))
    for a in aux:
        for au in a:
            aux2.append(au)
    tProductos = aux2
    for tProducto in tProductos:
        total = total + 1
        if tProducto.estado == 'Editado':
            parcial = parcial + 1
    if parcial == total:
        producto.pedido.lote.estado = "Editado"
        producto.pedido.lote.save()
    data = json.dumps({'status': "hola"})
    return HttpResponse(data, mimetype='application/json')

def edicion_pedido(request, lote):
    pedidos_edicion = Pedido.objects.filter(lote = Lote.objects.get(id = lote), estado = 'Edicion')
    pedidos_listos = Pedido.objects.filter(lote = Lote.objects.get(id = lote), estado = 'Editado')
    pedidos = []
    for pedido_edicion in pedidos_edicion:
        pedido = [pedido_edicion.codigo,0,0,pedido_edicion.id]
        productos_en_pedido = ProductoEventoPedido.objects.filter(pedido = pedido_edicion)
        for producto_en_pedido in productos_en_pedido:
            if producto_en_pedido.estado == 'Editado':
                pedido[1] = pedido[1] + 1
            pedido[2] = pedido[2] + 1
        pedidos.append(pedido)

    listos = []
    for pedido_listo in pedidos_listos:
        listo = [pedido_listo.codigo,0,0,pedido_listo.id]
        productos_en_pedido = ProductoEventoPedido.objects.filter(pedido = pedido_listo)
        for producto_en_pedido in productos_en_pedido:
            if producto_en_pedido.estado == 'Editado':
                listo[1] = listo[1]+1
            listo[2] = listo[2]+1
        listos.append(listo)
    return render_to_response('productos/edicion_pedidos.html', {'edicion': pedidos, 'listos':listos, 'lote': Lote.objects.get(id = lote)}, context_instance=RequestContext(request))

def administrar_lotes(request):
    lotes = Lote.objects.all()
    return render_to_response('productos/administrar_lotes.html', {'lotes':lotes}, context_instance=RequestContext(request))

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
        productosA.append(ProductoEventoPedido.objects.filter(pedido = pedido))
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