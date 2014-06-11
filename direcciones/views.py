import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from direcciones.models import *

@login_required(login_url='/')
def nueva_direccion(request):
    direcciones = Direccion.objects.all().exclude(id=1)
    if request.method == 'POST':
        latlng = request.POST.get('latlng').split(',')
        descripcion = request.POST.get('descripcion')
        nombre = request.POST.get('nombre')
        print nombre
        direccion = request.POST.get('direccion')
        lat=float(latlng[0])
        print latlng[0]
        lng =float(latlng[1])
        print lng
        dir = Direccion.objects.create(nombre=nombre, direccion=direccion, lat=float(lat), lon=float(lng),descripcion=descripcion)
        dir.save()

    else:
        pass
    return render_to_response('staff/nueva_direccion.html', {'direcciones': direcciones}, context_instance= RequestContext(request))

def guardar_direccion_ajax(request):
    nombre = request.GET.get('nombre')
    direccion = request.GET.get('direccion')
    latlng = request.GET.get('latlng').split(',')
    descripcion = request.GET.get('descripcion')
    lat = float(latlng[0])
    lng = float(latlng[1])
    dir = Direccion.objects.create(nombre=nombre, direccion=direccion, descripcion=descripcion, lat=lat, lon=lng)
    dir.save()
    lista = Direccion.objects.filter(id=dir.id)
    data= serializers.serialize('json', lista, fields=('nombre', 'direccion'))
    print data
    return HttpResponse(data,mimetype='aplication/json')

@login_required(login_url='/')
def libreta_incluida(request, id_input):
    direcciones = Direccion.objects.all().exclude(id=1)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        latlng = request.POST.get('latlng').split(',')
        descripcion = request.POST.get('descripcion')
        print nombre
        direccion = request.POST.get('direccion')
        lat=float(latlng[0])
        print latlng[0]
        lng =float(latlng[1])
        print lng
        dir = Direccion.objects.create(nombre=nombre, direccion=direccion, lat=float(lat), lon=float(lng),descripcion=descripcion)
        dir.save()
    else:
        pass
    return render_to_response('staff/incluir_libreta.html', {'direcciones': direcciones, 'id_input': id_input}, context_instance= RequestContext(request))

def obtener_direcciones():
    direcciones = Direccion.objects.all().exclude(id=1)
    return direcciones

def eliminar_direccion(request):
    direccion = Direccion.objects.get(id=request.GET.get('id'))
    if direccion.id != 1:
        direccion.delete()
    data = json.dumps({'status': 1})
    return HttpResponse(data,mimetype='aplication/json')