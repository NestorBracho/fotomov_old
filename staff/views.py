from staff.models import *
from tareas.models import *
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
		return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
	  else:
	    return render_to_response('staff/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
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

@login_required(login_url='/')
def escritorio(request):
    if Usuario.objects.get(usuario=request.user).privilegio.valor == 6:
        return HttpResponseRedirect('/calendario_de_eventos')
    user = request.user
    usuario = Usuario.objects.get(usuario=user)
    mis_tareas = Tarea.objects.filter(asignado=usuario.privilegio,lista='False',activa=True)
    #tareas = Tarea.objects.filter(activa=True)[15:]
    tareas = Tarea.objects.filter(activa=True)
    return render_to_response('escritorio.html', {'mis_tareas': mis_tareas, 'tareas': tareas}, context_instance=RequestContext(request))

@login_required(login_url='/')
def configurar_staff(request, creado):
    staff = Privilegios.objects.filter(valor=6)
    if request.method == 'POST':
        formulario = PrivilegioFrom(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            privilegio = Privilegios.objects.create(nombre=nombre, valor=6)
            privilegio.save()
            return render_to_response('staff/configurar_staff.html',{'privilegios':staff,'formulario': formulario, 'creado': creado, 'staffs': staff}, context_instance=RequestContext(request))
    else:
        formulario = PrivilegioFrom()
    return render_to_response('staff/configurar_staff.html', {'privilegios':staff,'formulario': formulario, 'creado': creado, 'staffs': staff}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_staff(request,id_borrar):
    eliminar = Privilegios.objects.get(id=id_borrar)
    if(eliminar.valor==6):
        eliminar.delete()
    return HttpResponseRedirect('/configurar_staff/0')

@login_required(login_url='/')
def modificar_staff(request,id_modificar):
    if(request.method=='POST'):
        modiStaff = PrivilegioFrom(request.POST)
        if(modiStaff.is_valid()):
            nomb = modiStaff.cleaned_data['nombre']
            staffViejo = Privilegios.objects.get(id=id_modificar)
            staffViejo.nombre=nomb
            staffViejo.save()
            return HttpResponseRedirect('/configurar_staff/0')
    else:
        if(Privilegios.objects.get(id=id_modificar)!=None):
            staff = Privilegios.objects.get(id=id_modificar)
            modiStaff = PrivilegioFrom(initial={'nombre':staff.nombre})
    return render_to_response('staff/modificar_staff.html',{'staff':modiStaff},context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_perfil(request, creado):


    usuario = request.user
    print usuario
    perfil = Usuario.objects.get(usuario=usuario)
    privilegio = perfil.privilegio
    archivos = ArchivoAdjunto.objects.filter(tipo_staff=privilegio)
    if perfil.equipos == None:
        perfil.equipos = Equipos.objects.create()
        perfil.save()
    if perfil.experiencia == None:
        perfil.experiencia = Experiencia.objects.create()
        perfil.save()
    if perfil.datos_pago == None:
        perfil.datos_pago = DatoDePago.objects.create()
        perfil.save()
    if request.method == 'POST':
        formulario = EditarUsuarioForm(request.POST)
        formulario2 = EquiposForm(request.POST)
        formulario3 = ExperienciaForm(request.POST)
        formulario4 = DatoDePagoForm(request.POST)
        if formulario.is_valid() and formulario2.is_valid() and formulario3.is_valid() and formulario4.is_valid():
            print "is valid"
            perfil.nombre = formulario.cleaned_data['nombre']
            perfil.apellido = formulario.cleaned_data['apellido']
            perfil.cedula = formulario.cleaned_data['cedula']
            perfil.email = formulario.cleaned_data['email']
            perfil.save()
            perfil.telefono_fijo = formulario.cleaned_data['telefono_fijo']
            perfil.telefono_celular = formulario.cleaned_data['telefono_celular']
            perfil.telefono_otro = formulario.cleaned_data['telefono_otro']
            perfil.twitter = formulario.cleaned_data['twitter']
            form2 = formulario2.save(commit=False)
            form3 = formulario3.save(commit=False)
            form4 = formulario4.save(commit=False)
            perfil.equipos.marca = form2.marca
            perfil.equipos.flash = form2.flash
            perfil.equipos.lente_1 = form2.lente_1
            perfil.equipos.lente_2 = form2.lente_2
            perfil.equipos.lente_3 = form2.lente_3
            perfil.equipos.memorias = form2.memorias
            perfil.equipos.iluminacion = form2.iluminacion
            perfil.equipos.otros = form2.otros
            perfil.equipos.save()
            perfil.experiencia.lightroom = form3.lightroom
            perfil.experiencia.photoshop = form3.photoshop
            perfil.experiencia.tipos = form3.tipos
            perfil.experiencia.save()
            perfil.datos_pago.banco = form4.banco
            perfil.datos_pago.tipo_de_cuenta = form4.tipo_de_cuenta
            perfil.datos_pago.numero = form4.numero
            perfil.datos_pago.save()
            return HttpResponseRedirect('/editar_perfil/2')
    else:
        formulario = EditarUsuarioForm(initial={'nombre': perfil.nombre, 'apellido': perfil.apellido, 'cedula': perfil.cedula,
                                                'email': perfil.email, 'telefono_fijo': perfil.telefono_fijo, 'telefono_celular': perfil.telefono_celular,
                                                'telefono_otro': perfil.telefono_otro, 'twitter': perfil.twitter})
        formulario2 = EquiposForm(initial={'marca': perfil.equipos.marca, 'flash': perfil.equipos.flash, 'lente_1': perfil.equipos.lente_1,
                                           'lente_2': perfil.equipos.lente_2, 'lente_3': perfil.equipos.lente_3, 'memorias': perfil.equipos.memorias,
                                           'iluminacion': perfil.equipos.iluminacion, 'otros': perfil.equipos.otros})
        formulario3 = ExperienciaForm(initial={'lightroom': perfil.experiencia.lightroom, 'photoshop': perfil.experiencia.photoshop, 'tipos': perfil.experiencia.tipos})
        formulario4 = DatoDePagoForm(initial={'banco': perfil.datos_pago.banco, 'tipo_de_cuenta': perfil.datos_pago.tipo_de_cuenta, 'numero': perfil.datos_pago.numero})
    return render_to_response('staff/perfil.html', {'archivos': archivos, 'formulario': formulario, 'formulario2': formulario2, 'formulario3': formulario3, 'formulario4': formulario4, 'creado': creado}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_perfil(request, id_staff):
    usuario = Usuario.objects.get(id=id_staff)
    return render_to_response('staff/ver_perfil.html', {'usuario': usuario}, context_instance=RequestContext(request))

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')

def eliminar_archivo_cliente(request, id_archivo):
    archivo = ArchivoAdjunto.objects.get(id=id_archivo)
    cliente = archivo.cliente
    archivo.delete()
    return HttpResponseRedirect('/ver_cliente/' + str(cliente.id))

def archivos_staff(request,id_staff):
    staff = Privilegios.objects.get(id=id_staff)
    archivos = ArchivoAdjunto.objects.filter(tipo_staff = staff)
    if request.method == 'POST':
        formulario = ArchivoAdjuntoStaff(request.POST, request.FILES)
        if formulario.is_valid():
            form = formulario.save(commit=False)
            form.tipo_staff = staff
            form.save()
            return HttpResponseRedirect('/archivos_staff/' + str(staff.id))
    else:
        formulario = ArchivoAdjuntoStaff()
    return render_to_response('staff/archivos_staff.html', {'formulario': formulario, 'archivos': archivos, 'staff': staff}, context_instance=RequestContext(request))

def eliminar_archivos_staff(request, id_archivo):
    archivo = ArchivoAdjunto.objects.get(id=id_archivo)
    staff = archivo.tipo_staff
    archivo.delete()
    return HttpResponseRedirect('/archivos_staff/' + str(staff.id))