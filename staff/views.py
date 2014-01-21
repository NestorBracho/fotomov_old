from staff.models import *
from staff.forms import RegisUsuarioForm, RegisNotificacion
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def contacto(request):
    formulario = RegisUsuarioForm()
    return render_to_response('staff/Regisform.html',{'formulario':formulario}, context_instance=RequestContext(request))

def notificacion(request):
    notificacion = RegisNotificacion()
    return render_to_response('staff/prueba.html',{'prueba':notificacion}, context_instance=RequestContext(request))

def lista_usuario(request):
    usuario = Usuario.objects.all()
    return render_to_response('staff/lista_usuario.html',{'lista':usuario}, context_instance=RequestContext(request))

def nuevo_usuario(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        formulario2 = RegisUsuarioForm(request.POST)
        if formulario.is_valid() and formulario2.is_valid():
            usu = formulario.save()
            nom = formulario2.cleaned_data['nombre']
            ape = formulario2.cleaned_data['apellido']
            ced = formulario2.cleaned_data['cedula']
            pri = formulario2.cleaned_data['privilegio']
            perfil = Usuario.objects.create(usuario = usu, nombre = nom, apellido = ape, cedula = ced, privilegio = pri)
            perfil.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
        formulario2 = RegisUsuarioForm()
    return render_to_response('staff/nuevo_usuario.html',{'formulario':formulario, 'formulario_regis':formulario2}, context_instance=RequestContext(request))

def eliminar_usuario(request, id_usuario):
    if Usuario.objects.get(id=id_usuario)!=None:
        usuario = Usuario.objects.get(id=id_usuario).delete()
    return render_to_response('staff/eliminar_usuario.html',{}, context_instance=RequestContext(request))

def modificar_usuario(request, id_usuario):
    if request.method=='POST':
        formulario2Modi = RegisUsuarioForm(request.POST)
        if formulario2Modi.is_valid():
            nom = formulario2Modi.cleaned_data['nombre']
            ape = formulario2Modi.cleaned_data['apellido']
            ced = formulario2Modi.cleaned_data['cedula']
            pri = formulario2Modi.cleaned_data['privilegio']
            perfil = Usuario.objects.get(id=id_usuario)
            perfil.nombre = nom
            perfil.apellido = ape
            perfil.cedula = ced
            perfil.privilegio = pri
            perfil.save()
            return HttpResponseRedirect('/')
    else:
        if Usuario.objects.get(id=id_usuario)!=None:
            varUsu = Usuario.objects.get(id=id_usuario)
            formulario2Modi = RegisUsuarioForm()
            return render_to_response('staff/modificar_usuario.html',{'usuario':varUsu, 'formulario_regis':formulario2Modi}, context_instance=RequestContext(request))