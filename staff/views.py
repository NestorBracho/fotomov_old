from staff.models import Usuario, Notificacion
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
    formulario = RegisUsuario()
    return render_to_response('staff/Regisform.html',{'formulario':formulario}, context_instance=RequestContext(request))

def notificacion(request):
    notificacion = RegisNotificacion()
    return render_to_response('staff/prueba.html',{'prueba':notificacion}, context_instance=RequestContext(request))

def lista_usuario(request):
    usuario = Usuario.objects.all()
    return render_to_response('staff/lista_usuario.html',{'lista':usuario})

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

	  perfil = Usuario.objects.create(usuario = usu, nombre = nom, apellido=ape, cedula = ced, privilegio = pri)

	  perfil.save()
	  return HttpResponseRedirect('/')
    else:
	formulario = UserCreationForm()
	formulario2 = RegisUsuarioForm()
    return render_to_response('staff/nuevo_usuario.html',{'formulario':formulario, 'formulario_regis':formulario2}, context_instance=RequestContext(request))

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
		return HttpResponseRedirect('/privado')
	    else:
		return render_to_response('noactivo.html', context_instance=RequestContext(request))
	  else:
	    return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
	formulario = AuthenticationForm()
    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))



