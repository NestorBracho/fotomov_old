from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from direcciones.models import *

def nueva_direccion(request):
    direcciones = Direccion.objects.all()
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