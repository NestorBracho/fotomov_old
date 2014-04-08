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
    productos_edicion = ProductoEventoPedido.objects.filter(estado = "Edicion")
    productos_editados = ProductoEventoPedido.objects.filter(estado = "Editado")
    productos = []
    for productos_edicio in productos_edicion:
        productos.append(productos_edicio)
    for productos_editado in productos_editados:
        productos.append(productos_editado)
    return render_to_response('productos/edicion_lotes.html', {'productos': productos}, context_instance=RequestContext(request))

def edicion_productos(request, pedido):
    pedidos_edicion = ProductoEventoPedido.objects.filter(pedido = Pedido.objects.get(id = pedido), estado = 'Edicion')
    pedidos_editados = ProductoEventoPedido.objects.filter(pedido = Pedido.objects.get(id = pedido), estado = 'Editado')
    return render_to_response('productos/edicion_productos.html', {'edicion': pedidos_edicion, 'editados': pedidos_editados}, context_instance=RequestContext(request))

def cambiar_estado_producto_edicion_a_editado(request):
    producto = ProductoEventoPedido.objects.get(id = request.GET['iden'])
    producto.estado = 'Editado'
    producto.save()
    data = json.dumps({'status': "hola"})
    return HttpResponse(data, mimetype='application/json')