from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from manager.forms import *
from manager.models import *
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url='/')
def pedidos(request):
  usuario = request.user
  pedidos = Pedido.objects.filter(usuario=usuario)
  return render_to_response('pedidos.html',{'pedidos':pedidos}, context_instance=RequestContext(request))

def hacer_pedido(request):
  mensaje = ""
  if request.method == 'POST':
    formulario = AuthenticationForm(request.POST)
    pedido_form = PedidoForm(request.POST)
    if '_ingresar' in request.POST:
      if formulario.is_valid:
        usuario = request.POST['username']
        clave = request.POST['password']
        print usuario
        print clave
        usuario = usuario.lower()
        acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
          if acceso.is_active:
            login(request,acceso)
            return HttpResponseRedirect('/pedidos')
          else:
            formulario = AuthenticationForm()
            error_log = "usuario bloqueado"
            return render_to_response('index.html',{'formulario':formulario,'error_log':error_log,'pedido_form': pedido_form}, context_instance=RequestContext(request))
        else:
          formulario = AuthenticationForm()
          error_log = "usuario o clave incorrecto"
          return render_to_response('index.html',{'formulario':formulario,'error_log':error_log,'pedido_form': pedido_form}, context_instance=RequestContext(request))
    else:
      print "estoy en pedido"
      if pedido_form.is_valid(): 
        email = str(pedido_form.cleaned_data['user_email']).lower()
        if User.objects.filter(username=email):
          mensaje = "el email ya existe por favor inicie sesion para hacer un pedido"
          return render_to_response('index.html',{'formulario':formulario,'mensaje':mensaje,'pedido_form': pedido_form}, context_instance=RequestContext(request))
        else:
          #el email es nuevo
          password = pedido_form.cleaned_data['user_pass']
          if password == pedido_form.cleaned_data['user_pass2']:
            repuestos = request.POST.getlist('alist')
            print "ahi va la longitud"
            print len(repuestos)
            if len(repuestos) > 0 and repuestos[0] != "" and repuestos[1]!= "":
              #los password son iguales
              user = User.objects.create_user(email,email,password)
              user.first_name = pedido_form.cleaned_data['user_nombre']
              user.last_name =  pedido_form.cleaned_data['user_apellido']
              user.save()
              telefono = Telefono_Clientes.objects.create(user=user,cod_telefono = pedido_form.cleaned_data['user_telfop'],telefono=pedido_form.cleaned_data['user_telf'])
              telefono.save()
              vehiculo = Vehiculo.objects.create(usuario=user,marca=pedido_form.cleaned_data['marca'],modelo=pedido_form.cleaned_data['modelo'],year=pedido_form.cleaned_data['year'],serial=pedido_form.cleaned_data['serial'],version=pedido_form.cleaned_data['version'])
              vehiculo.save()

              print len(repuestos)
              i = 0
              while i < len(repuestos):
                repuesto = Repuesto.objects.create(vehiculo=vehiculo,nombre=repuestos[i],numero=repuestos[i+1])
                repuesto.save()
                pedido = Pedido.objects.create(repuesto=repuesto,usuario=user,vehiculo=vehiculo)
                pedido.save()
                i += 2
                #repuesto = Repuesto.objects.create(vehiculo=vehiculo,nombre=pedido_form.cleaned_data['year'])
            else:
              mensaje = "debe pedir por lo menos un repuesto"
              return render_to_response('index.html',{'formulario':formulario,'mensaje':mensaje,'pedido_form': pedido_form}, context_instance=RequestContext(request))
          else:
            mensaje = "las claves no coinciden"
            return render_to_response('index.html',{'formulario':formulario,'mensaje':mensaje,'pedido_form': pedido_form}, context_instance=RequestContext(request))
      else:
        mensaje = "algunos campos no son validos"
  else:
    formulario = AuthenticationForm()
    pedido_form = PedidoForm()

  return render_to_response('index.html', { 'formulario':formulario,'pedido_form': pedido_form,'mensaje':mensaje}, context_instance=RequestContext(request))

@login_required(login_url='/')
def datos_client(request):
  user = request.user
  lista_pedidos = Pedido.objects.filter(usuario=user)
  try:
    tenia_telefono = 1
    telefono_user = Telefono_Clientes.objects.get(user=user)
  except ObjectDoesNotExist:
    tenia_telefono = 0
  cod_telefono = '0414'
  telefono = ''
  if request.method == 'POST':
      datos_form = DatosClientForm(request.POST,request.FILES)
      formulario = AuthenticationForm(request.POST)
      if formulario.is_valid:
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        clave = request.POST['clave']
        clave_confirmacion = request.POST['clave_confirmacion']
        cod_telefono = request.POST['cod_telefono']
        telefono = request.POST['telefono']
        email = request.POST['email']
        
        if clave == clave_confirmacion :
          #user.username = username
          user.email = email
          user.first_name = nombre
          user.last_name = apellido
          user.set_password(clave)
          user.save()
          
          if telefono == '':
            if tenia_telefono == 1:
              telefono_user.delete()          
          
          if telefono != '':
            if tenia_telefono == 1:
              telefono_user.delete()
            tlf = Telefono_Clientes.objects.create(user=user,cod_telefono=cod_telefono,telefono=telefono)
            tlf.save()
          
          return render_to_response('datos.html',{'formulario':formulario,'datos_form': datos_form,'lista_pedidos':lista_pedidos},context_instance=RequestContext(request)) 
        
        else:
          mensaje_contrasena = '* Verifique las contrasenas'
          return render_to_response('datos.html',{'formulario':formulario,'datos_form': datos_form,'lista_pedidos':lista_pedidos,
          'mensaje_contrasena':mensaje_contrasena},context_instance=RequestContext(request))
      else:
        mensaje = "Los campos marcados abajo no se han introducido correctamente"   
  else:
      # Formulario inicial
      if tenia_telefono == 1:
        datos_form = DatosClientForm(initial={'nombre':user.first_name,'apellido':user.last_name,
      'cod_telefono':telefono_user.cod_telefono,'telefono':telefono_user.telefono,'email':user.email})
      else:
        datos_form = DatosClientForm(initial={'nombre':user.first_name,'apellido':user.last_name,'email':user.email})
      formulario = AuthenticationForm()
  return render_to_response('datos.html', {'formulario':formulario,'datos_form': datos_form,'lista_pedidos':lista_pedidos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def pedidos_admin(request):
  lista_pedidos = Pedido.objects.all()
  return render_to_response('todos_pedidos.html', {'lista_pedidos':lista_pedidos}, context_instance=RequestContext(request))
  
def modif_pedidos(request):
  lista_recibidos = request.POST.getlist('lista_recibidos')  
  lista_modificados = request.POST.getlist('lista_modificados')
  
  for li in lista_modificados:
    pedido = Pedido.objects.get(id=li)
    id_status = 'status' + str(li)
    status = request.POST.get(id_status)
    print status
    id_precio = 'precio' + str(li)
    precio = request.POST.get(id_precio)
    if li in lista_recibidos:
      pedido.recibido = True
    else:
      pedido.recibido = False
    pedido.status = status
    pedido.precio = precio
    pedido.save()
  
  return HttpResponseRedirect('/todos_pedidos')
