from staff.models import *
from staff.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def contacto(request):
    formulario = RegisUsuario()
    return render_to_response('staff/Regisform.html',{'formulario':formulario}, context_instance=RequestContext(request))

def notificacion(request):
    notificacion = RegisNotificacion()
    return render_to_response('staff/prueba.html',{'prueba':notificacion}, context_instance=RequestContext(request))

def lista_usuario(request, creado):
    usuario = Usuario.objects.all()
    return render_to_response('staff/lista_usuario.html',{'lista':usuario, 'creado':creado}, context_instance=RequestContext(request))

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        formulario2 = RegisUsuarioForm(request.POST)
        if formulario.is_valid() and formulario2.is_valid():
            usu = formulario.save()
            nom = formulario2.cleaned_data['nombre']
            ape = formulario2.cleaned_data['apellido']
            ced = formulario2.cleaned_data['cedula']
            ema = formulario2.cleaned_data['email']
            pri = formulario2.cleaned_data['privilegio']
            try:
                perfil = Usuario.objects.create(usuario = usu, email=ema, nombre=nom, apellido=ape, cedula=ced, privilegio=pri)
                perfil.save()
                return HttpResponseRedirect('/listar_usuario/1')
            except:
                usu.delete()
                #poner aqui error de cedula repetida
                #formulario2.errors['cedula'] = form.error_class(["error"])
                pass
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
		return HttpResponseRedirect('/escritorio')
	    else:
		return render_to_response('noactivo.html', context_instance=RequestContext(request))
	  else:
	    return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
	formulario = AuthenticationForm()
    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

def eliminar_usuario(request, id_usuario):
    #if Usuario.objects.get(id=id_usuario)!=None:
    u = User.objects.get(username__exact=Usuario.objects.get(id=id_usuario).usuario.username)
    Usuario.objects.get(id=id_usuario).delete()
    u.delete()
    return HttpResponseRedirect('/listar_usuario/3')

@login_required(login_url='/')
def modificar_usuario(request, id_usuario):
    varUsu = Usuario.objects.get(id=id_usuario)
    varUser = User.objects.get(username__exact=varUsu.usuario.username)
    if request.method=='POST':
        formularioModi = PasswordChangeForm(user=varUser, data=request.POST)
        formulario2Modi = RegisUsuarioForm(request.POST)
        if formulario2Modi.is_valid():
            #usu = formularioModi.save(commit=False)
            print request.user
            nom = formulario2Modi.cleaned_data['nombre']
            ape = formulario2Modi.cleaned_data['apellido']
            ced = formulario2Modi.cleaned_data['cedula']
            pri = formulario2Modi.cleaned_data['privilegio']
            ema = formulario2Modi.cleaned_data['email']
            perfil = Usuario.objects.get(id=id_usuario)
            perfil.nombre = nom
            perfil.apellido = ape
            perfil.cedula = ced
            perfil.privilegio = pri
            perfil.email = ema
            perfil.save()
            return HttpResponseRedirect('/listar_usuario/2')
    else:
        if Usuario.objects.get(id=id_usuario)!=None:
            #formularioModi =  PasswordChangeForm(SetPasswordForm(User.objects.get(username=Usuario.objects.get(id=id_usuario).usuario.username)))
            formulario2Modi = RegisUsuarioForm(initial={'nombre': varUsu.nombre, 'apellido': varUsu.apellido, 'cedula': varUsu.cedula, 'email': varUsu.email, 'privilegio': varUsu.privilegio.valor})
    return render_to_response('staff/modificar_usuario.html',{'usuario':varUsu, 'formulario_regis':formulario2Modi}, context_instance=RequestContext(request))

def ver_usuario(request, id_usuario):
    return render_to_response('staff/ver_usuario.html', {'usuario':Usuario.objects.get(id=id_usuario)}, context_instance=RequestContext(request))

def escritorio(request):
    return render_to_response('escritorio.html', {}, context_instance=RequestContext(request))
