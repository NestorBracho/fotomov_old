from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from marca.forms import *
from marca.models import *

def nueva_marca(request):
    if request.method == 'POST':
        formulario = MarcaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            marca = Marca.objects.create(nombre=nombre)
            return HttpResponseRedirect('/listar_marcas/1')
    else:
        pass
    formulario = MarcaForm()
    return render_to_response('marca/nueva_marca.html', {'formulario': formulario}, context_instance=RequestContext(request))

def editar_marca(request, id_marca):
    if Marca.objects.filter(id=id_marca):
        marca = Marca.objects.get(id=id_marca)
    else:
        return HttpResponseRedirect('/listar_marcas/2')
    if request.method == 'POST':
        formulario = MarcaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            marca.nombre = nombre
            marca.save()
            return HttpResponseRedirect('/listar_marcas/2')
    else:
        formulario = MarcaForm(initial={'nombre': marca.nombre})
    return render_to_response('marca/nueva_marca.html', {'formulario': formulario}, context_instance=RequestContext(request))

def listar_marcas(request, creado):
    marcas = Marca.objects.all()
    return render_to_response('marca/listar_marcas.html', {'marcas': marcas, 'creado': creado}, context_instance=RequestContext(request))

def ver_marca(request, id_marca, creado):
    if Marca.objects.filter(id=id_marca):
        marca = Marca.objects.get(id=id_marca)
        submarcas = SubMarca.objects.filter(marca=marca)
    else:
        return HttpResponseRedirect('/listar_marcas/0')
    return render_to_response('marca/ver_marca.html', {'marca': marca, 'submarcas': submarcas, 'creado': creado}, context_instance=RequestContext(request))

def nueva_submarca(request, id_marca):
    if Marca.objects.filter(id=id_marca):
        marca = Marca.objects.get(id=id_marca)
    else:
        return HttpResponseRedirect('/listar_marcas/0')
    if request.method == 'POST':
        formulario = SubMarcaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            submarca = SubMarca.objects.create(nombre=nombre, marca= marca)
            print '/ver_marca/' + id_marca + '/1'
            return HttpResponseRedirect('/ver_marca/' + id_marca + '/1')
    else:
        formulario = SubMarcaForm()
    return render_to_response('marca/nueva_submarca.html', {'formulario': formulario, 'marca': marca}, context_instance=RequestContext(request))

def editar_submarca(request, id_submarca):
    if SubMarca.objects.filter(id=id_submarca):
        submarca = SubMarca.objects.get(id=id_submarca)
        old = submarca.marca.id
    else:
        return HttpResponseRedirect('/var_marca/' + id_submarca + '/2')
    if request.method == 'POST':
        formulario = EditarSubMarcaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            marca = formulario.cleaned_data['marca']
            submarca.nombre = nombre
            submarca.marca = marca
            submarca.save()
            return HttpResponseRedirect('/ver_marca/' + str(old) + '/1')
    else:
        formulario = EditarSubMarcaForm(initial = {'nombre': submarca.nombre, 'marca': submarca.marca})
    return render_to_response('marca/editar_submarca.html', {'formulario': formulario, 'submarca': submarca}, context_instance=RequestContext(request))

def eliminar_marca(request,id_marca):
    if Marca.objects.filter(id=id_marca):
        #Marca.objects.get(id=id_marca).delete()
        pass
    return HttpResponseRedirect('/listar_marcas/3')
