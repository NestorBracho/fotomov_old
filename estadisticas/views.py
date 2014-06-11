from django.shortcuts import render
from estadisticas.models import *
from estadisticas.forms import *
from marca.models import *
from clientes.models import *
from evento.models import *
from administracion.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
import datetime
import json

#Vista de las estadisticas de las marcas
@login_required(login_url='/')
def estadisticas_marcas(request):

	mesesF = MesesForm()

	#Query para las marcas
	marcas = Marca.objects.all()
	marcas_total = []

	#Informacion de las marcas
	for marca in marcas:

		#Inicializacion de variables
		submarcas = 0
		macros = 0
		eventos = 0
		eventos_total = 0
		egresos_evento = 0
		total_evento = 0
		mes = ''
		ano = ''
		mes_anterior = ''
		fecha_actual = ''
		producto_evento = []
		pedidos = []

		#Informacion de las submarcas
		try:
			submarcas = SubMarca.objects.filter(marca=marca)
		except:
			error = 'Esta marca no posee submarcas'

		for submarca in submarcas:
			
			#Informacion de macroclientes
			try:
				macros = MacroCliente.objects.filter(submarca=submarca)
			except:
				error = 'Esta submarca no posee macroclientes'

			for macro in macros:

				#Revisa si se filtro por un mes especifico
				if request.method == 'POST':
					mesesF = MesesForm(request.POST)
					if mesesF.is_valid():
						mes = mesesF.cleaned_data['mes']

				#Caso en el que se coloco un mes en el filtro
				if len(mes) > 0:
					fecha_actual = datetime.datetime.now()
					mes_anterior = 12 - int(fecha_actual.month)
					eventos = Evento.objects.filter(macrocliente=macro, funcion__dia__month=mes).distinct()
					eventos_total += len(eventos)
				else:
					eventos = Evento.objects.filter(macrocliente__id=macro.id)
					eventos_total += len(eventos)	

				#Informacion de los eventos
				for evento in eventos:
					
					#Informacion de los pedidos del evento
					try:
						producto_evento = ProductoEvento.objects.filter(evento=evento)
					except:
						error = ''

					#Informacion de los productos de cada evento
					for producto in producto_evento:

						productos_evento_pedido = ProductoEventoPedido.objects.filter(producto=producto)

						#Informacion de los productos pedidos en cada evento
						for producto_pedido in productos_evento_pedido:
							pedidos = Pedido.objects.filter(num_pedido=producto_pedido.num_pedido, fue_pagado=True)

							#Informacion de los pedidos de cada evento
							for pedido in pedidos:
								total_evento = total_evento + pedido.total
			
					#Informacion de los gastos o egresos de cada evento
					try:
						gastos_evento = GastoEvento.objects.filter(evento=evento)
					except:
						error = 'Este evento no tiene gastos asociados'
					
					for gasto in gastos_evento:
						egresos_evento = egresos_evento + gasto.monto

			marcas_total.append((marca.id, marca.nombre, len(submarcas), len(macros), eventos_total, total_evento, egresos_evento, total_evento-egresos_evento))

	ctx = {'marcas':marcas_total, 'MesesForm': mesesF}
	return render_to_response('estadisticas/marcas.html', ctx, context_instance = RequestContext(request))

#Vista de las estadisticas de las submarcas de una marca
@login_required(login_url='/')
def estadisticas_submarcas(request, id_marca):

	mesesF = MesesForm()
	submarcas = []
	submarcas_total = []

	#Informacion de las submarcas
	try:
		submarcas = SubMarca.objects.filter(marca__id=id_marca)
	except:
		error = 'No existen submarcas en esta marca'

	for submarca in submarcas:
		mes = ''
		macros = 0
		eventos = 0
		eventos_total = 0
		egresos_evento = 0
		total_evento = 0
		
		#Informacion de macroclientes
		try:
			macros = MacroCliente.objects.filter(submarca=submarca)
		except:
			error = 'Esta submarca no posee macroclientes'

		for macro in macros:


			#Revisa si se filtro por un mes especifico
			if request.method == 'POST':
				mesesF = MesesForm(request.POST)
				if mesesF.is_valid():
					mes = mesesF.cleaned_data['mes']

			#Caso en el que se coloco un mes en el filtro
			if len(mes) > 0:
				fecha_actual = datetime.datetime.now()
				mes_anterior = 12 - int(fecha_actual.month)
				eventos = Evento.objects.filter(macrocliente=macro, funcion__dia__month=mes).distinct()
				eventos_total += len(eventos)
			else:
				eventos = Evento.objects.filter(macrocliente__id=macro.id)
				eventos_total += len(eventos)

			#Informacion de los eventos
			for evento in eventos:
				
				#Informacion de los pedidos del evento
				try:
					producto_evento = ProductoEvento.objects.filter(evento=evento)
				except:
					error = ''

				#Informacion de los productos de cada evento
				for producto in producto_evento:
					productos_evento_pedido = ProductoEventoPedido.objects.filter(producto=producto)

					#Informacion de los productos pedidos en cada evento
					for producto_pedido in productos_evento_pedido:
						pedidos = Pedido.objects.filter(num_pedido=producto_pedido.num_pedido, fue_pagado=True)

						#Informacion de los pedidos de cada evento
						for pedido in pedidos:
							total_evento = total_evento + pedido.total
		
				#Informacion de los gastos o egresos de cada evento
				try:
					gastos_evento = GastoEvento.objects.filter(evento=evento)
				except:
					error = 'Este evento no tiene gastos asociados'
				
				for gasto in gastos_evento:
					egresos_evento = egresos_evento + gasto.monto

		submarcas_total.append((submarca.id, submarca.nombre, len(macros), eventos_total, total_evento, egresos_evento, total_evento-egresos_evento))

	ctx = {'submarcas':submarcas_total, 'MesesForm': mesesF}
	return render_to_response('estadisticas/submarcas.html', ctx, context_instance = RequestContext(request))

#Vista de las estadisticas de los macroclientes asociados a una submarca
@login_required(login_url='/')
def estadisticas_macros(request, id_submarca):
	
	mesesF = MesesForm()
	macros = []
	macros_total = []
		
	#Informacion de macroclientes
	try:
		macros = MacroCliente.objects.filter(submarca__id=id_submarca)
	except:
		error = 'Esta submarca no posee macroclientes'

	for macro in macros:
		mes = ''
		eventos = 0
		eventos_total = 0
		egresos_evento = 0
		total_evento = 0

		#Revisa si se filtro por un mes especifico
		if request.method == 'POST':
			mesesF = MesesForm(request.POST)
			if mesesF.is_valid():
				mes = mesesF.cleaned_data['mes']

		#Caso en el que se coloco un mes en el filtro
		if len(mes) > 0:
			fecha_actual = datetime.datetime.now()
			mes_anterior = 12 - int(fecha_actual.month)
			eventos = Evento.objects.filter(macrocliente=macro, funcion__dia__month=mes).distinct()
			eventos_total += len(eventos)
		else:
			eventos = Evento.objects.filter(macrocliente__id=macro.id)
			eventos_total += len(eventos)

		#Informacion de los eventos
		for evento in eventos:
			
			#Informacion de los pedidos del evento
			try:
				producto_evento = ProductoEvento.objects.filter(evento=evento)
			except:
				error = ''

			#Informacion de los productos de cada evento
			for producto in producto_evento:
				productos_evento_pedido = ProductoEventoPedido.objects.filter(producto=producto)

				#Informacion de los productos pedidos en cada evento
				for producto_pedido in productos_evento_pedido:
					pedidos = Pedido.objects.filter(num_pedido=producto_pedido.num_pedido, fue_pagado=True)

					#Informacion de los pedidos de cada evento
					for pedido in pedidos:
						total_evento += pedido.total
	
			#Informacion de los gastos o egresos de cada evento
			try:
				gastos_evento = GastoEvento.objects.filter(evento=evento)
			except:
				error = 'Este evento no tiene gastos asociados'
			
			for gasto in gastos_evento:
				egresos_evento += gasto.monto

		macros_total.append((macro.id, macro.nombre, eventos_total, total_evento, egresos_evento, total_evento-egresos_evento))

	ctx = {'macros':macros_total, 'MesesForm': mesesF}
	return render_to_response('estadisticas/macroclientes.html', ctx, context_instance = RequestContext(request))

#Vista de las estadisticas de los macroclientes asociados a una submarca
@login_required(login_url='/')
def estadisticas_eventos(request, id_macro):
	
	mes = ''
	mesesF = MesesForm()
	eventos = []
	eventos_total = []

	#Revisa si se filtro por un mes especifico
	if request.method == 'POST':
		mesesF = MesesForm(request.POST)
		if mesesF.is_valid():
			mes = mesesF.cleaned_data['mes']

	#Caso en el que se coloco un mes en el filtro
	if len(mes) > 0:
		fecha_actual = datetime.datetime.now()
		mes_anterior = 12 - int(fecha_actual.month)
		eventos = Evento.objects.filter(macrocliente__id=id_macro, funcion__dia__month=mes).distinct()
	else:
		eventos = Evento.objects.filter(macrocliente__id=id_macro)

	#Informacion de los eventos
	for evento in eventos:

		egresos_evento = 0
		total_evento = 0
		
		#Informacion de los pedidos del evento
		try:
			producto_evento = ProductoEvento.objects.filter(evento=evento)
		except:
			error = ''

		#Informacion de los productos de cada evento
		for producto in producto_evento:
			productos_evento_pedido = ProductoEventoPedido.objects.filter(producto=producto)

			#Informacion de los productos pedidos en cada evento
			for producto_pedido in productos_evento_pedido:
				pedidos = Pedido.objects.filter(num_pedido=producto_pedido.num_pedido, fue_pagado=True)

				#Informacion de los pedidos de cada evento
				for pedido in pedidos:
					total_evento += pedido.total

		#Informacion de los gastos o egresos de cada evento
		try:
			gastos_evento = GastoEvento.objects.filter(evento=evento)
		except:
			error = 'Este evento no tiene gastos asociados'
		
		for gasto in gastos_evento:
			egresos_evento += gasto.monto

		eventos_total.append((evento.id, evento.nombre, total_evento, egresos_evento, total_evento-egresos_evento))

	ctx = {'eventos':eventos_total, 'MesesForm': mesesF}
	return render_to_response('estadisticas/eventos.html', ctx, context_instance = RequestContext(request))

#Vista de las estadisticas de los clientes
@login_required(login_url='/')
def estadisticas_clientes(request):

	#Inicializacion de variables y demas
	mesesF = MesesForm()
	clientes = Cliente.objects.all()
	pedidos = []
	clientes_total = []

	#Extraccion de datos del cliente
	for cliente in clientes:

		productos_total = 0
		total_pedidos = 0
		total_pedidos_pagados = 0
		total_pedidos_morosos = 0

		pedidos = Pedido.objects.filter(cliente__id=cliente.id)

		#Extraccion de los pedidos
		for pedido in pedidos:

			producto_evento_pedidos = ProductoEventoPedido.objects.filter(num_pedido=pedido.num_pedido)
			productos_total += producto_evento_pedidos.count()
			total_pedidos += pedido.total

			#Datos de pago de pedidos
			if pedido.fue_pagado == True:
				total_pedidos_pagados += pedido.total
			else:
				total_pedidos_morosos += pedido.total

		clientes_total.append((cliente.nombres, total_pedidos_pagados, total_pedidos_morosos, pedidos.count(), productos_total))

	ctx = {'clientes':clientes_total, 'MesesForm': mesesF}
	return render_to_response('estadisticas/clientes.html', ctx, context_instance = RequestContext(request))


#Vista de las estadisticas del staff
@login_required(login_url='/')
def estadisticas_staff(request):

	#Inicializacion de variables y demas
	sForm = StaffForm()
	filtro_privilegio = ''

	#Tipos de staff que se filtran
	if request.method == 'POST' :
		sForm = StaffForm(request.POST)

		if sForm.is_valid() :
			filtro_privilegio = sForm.cleaned_data['privilegios']

	if len(filtro_privilegio) > 0:
		staffs = Usuario.objects.filter(privilegio__nombre=filtro_privilegio).order_by('privilegio__nombre')
	else:
		staffs = Usuario.objects.all().order_by('privilegio__nombre')

	staffs_total = []
	eventos_postulado = []
	pagos_eventos = []

	#Extraccion de datos del staff
	for staff in staffs:
		eventos_contratado = 0
		pagado = 0
		deuda = 0

		eventos_postulados = AsistenciaStaffFuncion.objects.filter(usuario__id=staff.id)

		#Informacion de los eventos que se postulo o se pidio el staff
		for evento in eventos_postulados:

			#Caso en que el usuario fue convocado y asistio
			if evento.asistencia==True and evento.fue_convocado==True:
				eventos_contratado += 1

			#Informacion de pagos de eventos al usuario staff
			pagos_eventos = GastoEvento.objects.filter(usuario=evento.usuario)

			for pago in pagos_eventos:

				#Caso de pagos realizados
				if pago.fue_pagado==True:
					pagado += pago.monto
				else:
					deuda += pago.monto

		staffs_total.append((staff.nombre, eventos_postulados.count(), eventos_contratado, pagado, deuda))

	ctx = {'staffs':staffs_total, 'StaffForm': sForm}
	return render_to_response('estadisticas/staff.html', ctx, context_instance = RequestContext(request))


#Vista de los graficos
@login_required(login_url='/')
def estadisticas_grafico_macro(request):

	flag = False
	data = []
	magnitud = ''
	graficoForm = GraficoMacroclienteForm()

	#Estadisticas de gastos e ingresos
	marcas = Marca.objects.all()
	submarcas = SubMarca.objects.all()
	macros = MacroCliente.objects.all()

	#Verificacion que se hizo un post en la pagina
	if request.method == 'POST':

		graficoForm = GraficoMacroclienteForm(request.POST)

		if graficoForm.is_valid() :
			magnitud = graficoForm.cleaned_data['magnitud']
			macrocliente = graficoForm.cleaned_data['macrocliente']

			#Verificacion de que cada campo o puede estar en blanco o en la opcion inicial
			if magnitud != '' and macrocliente != '':
				flag = True
				data = grafico_macro(magnitud, macrocliente)

	ctx = {'graficoForm' : graficoForm, 'marcas':marcas, 'submarcas':submarcas,
		'macroclientes':macros,'flag':flag,'data': data,'magnitud': magnitud,}

	return render_to_response('estadisticas/grafico_macro.html', ctx, context_instance = RequestContext(request))

#Vista para manejar la informacion del grafico de macroclientes
def grafico_macro(magnitud, id_macro):

	i = 0
	egresos = 0
	ingresos = 0
	ganancias = 0
	total_evento = 0
	data = []
	macro = []
	eventos = []
	ingresos = []
	funciones = []	
	meses_egresos = []
	meses_ingresos = []
	meses_ganancias = []
	producto_evento = []
	egresos_funcion = []
	ingresos_funcion = []
	ganancias_funcion = []
	meses = (
		('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), 
		('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), 
		('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), 
		('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'),
	)

	#Extraccion de los datos del macrocliente elegido
	try:
		macro = MacroCliente.objects.get(id=id_macro);
	except:
		error = ''

	#Verificacion del caso para ingresos
	if magnitud == 'ingresos':

		#Extraccion de datos de los eventos y funciones
		try:
			eventos = Evento.objects.filter(macrocliente=macro)
		except:
			error = ''

		#Cada mes en el que se encuentra la magnitud especifica
		for mes in meses:

			#Cada evento en el que se encuentran las funciones
			for evento in eventos:

				ingresos = 0
				funciones = Funcion.objects.filter(evento=evento, dia__month=mes[0]).order_by('dia')

				#Extraccion de los ingresos de cada funcion de cada evento
				for funcion in funciones:

					#Informacion de los pedidos del evento
					try:
						producto_evento = ProductoEvento.objects.filter(evento=funcion.evento)
					except:
						error = ''
					
					#Informacion de los productos de cada evento
					for producto in producto_evento:
						productos_evento_pedido = ProductoEventoPedido.objects.filter(producto=producto)

						#Informacion de los productos pedidos en cada evento
						for producto_pedido in productos_evento_pedido:
							pedidos = Pedido.objects.filter(num_pedido=producto_pedido.num_pedido)
							
							#Informacion de los pedidos de cada evento
							for pedido in pedidos:
								ingresos += pedido.total

				#Verificacion de que existe ingreso en el mes especifico
				if ingresos != 0:
					meses_ingresos.append((mes[1], ingresos))
				else:
					meses_ingresos.append((mes[1], ingresos))

		#Objeto Json que se retornara
		for item in meses_ingresos:
			data.append({'y':item[0], magnitud:str(item[1])})

	#Verificacion del caso para egresos
	elif magnitud == 'egresos':

		#Extraccion de datos de los eventos y funciones
		try:	
			eventos = Evento.objects.filter(macrocliente=macro)
		except:
			error = ''

		#Meses de cada magnitud
		for mes in meses:

			#Cada evento en el que se encuentran las funciones
			for evento in eventos:

				egresos = 0
				funciones = Funcion.objects.filter(evento=evento, dia__month=mes[0]).order_by('dia')

				#Extraccion de los egresos de cada funcion de cada evento
				for funcion in funciones:

					#Informacion de los gastos o egresos de cada evento
					try:
						egresos_funcion = GastoEvento.objects.get(evento=funcion.evento, fue_pagado=True)
					except:
						error = 'Este evento no tiene egresos asociados'

					#Verificacion de que encontro un egreso
					if egresos_funcion != []:
						egresos += egresos_funcion.monto

				if egresos != 0:
					meses_egresos.append((mes[1], egresos))
				else:
					meses_egresos.append((mes[1], egresos))
			
		#Objeto Json que se retornara
		for item in meses_egresos:
			data.append({'y':item[0], magnitud:str(item[1])})

	#Verificacion del caso para ganancias
	elif magnitud == 'ganancias':

		#Extraccion de datos de los eventos y funciones
		try:
			eventos = Evento.objects.filter(macrocliente=macro)
		except:
			error = ''

		#Meses de cada magnitud
		for mes in meses:

			for evento in eventos:

				egresos = 0
				ingresos = 0
				funciones = Funcion.objects.filter(evento=evento, dia__month=mes[0]).order_by('dia')

				#Extraccion de los ingresos de cada funcion de cada evento
				for funcion in funciones:

					#Informacion de los pedidos del evento
					try:
						producto_evento = ProductoEvento.objects.filter(evento=funcion.evento)
					except:
						error = ''
					
					#Informacion de los productos de cada evento
					for producto in producto_evento:
						productos_evento_pedido = ProductoEventoPedido.objects.filter(producto=producto)

						#Informacion de los productos pedidos en cada evento
						for producto_pedido in productos_evento_pedido:
							pedidos = Pedido.objects.filter(num_pedido=producto_pedido.num_pedido)
							
							#Informacion de los pedidos de cada evento
							for pedido in pedidos:
								ingresos += pedido.total

					#Informacion de los gastos o egresos de cada evento
					try:
						egresos_funcion = GastoEvento.objects.get(evento=funcion.evento, fue_pagado=True)
					except:
						error = 'Este evento no tiene egresos asociados'

					#Verificacion de que encontro un egreso
					if egresos_funcion != []:
						egresos += egresos_funcion.monto

				#Verificacion de que existe ingreso en el mes especifico
				if ingresos != 0 or egresos != 0:

					meses_ganancias.append((mes[1], ingresos-egresos))
				else:
					meses_ganancias.append((mes[1], ingresos-egresos))

		#Objeto Json que se retornara
		for item in meses_ganancias:
			data.append({'y':item[0], magnitud:str(item[1])})

	#Objeto json a devolver para el grafico
	return json.dumps(data)

#Vista de los graficos
def estadisticas_grafico_marca(request):

	flag = False
	data = []
	magnitud = ''
	graficoForm = GraficoMarcaForm()

	#Estadisticas de gastos e ingresos
	marcas = Marca.objects.all()

	#Verificacion que se hizo un post en la pagina
	if request.method == 'POST':

		graficoForm = GraficoMarcaForm(request.POST)

		if graficoForm.is_valid() :
			magnitud = graficoForm.cleaned_data['magnitud']
			marca = graficoForm.cleaned_data['marca']

			#Verificacion de que cada campo o puede estar en blanco o en la opcion inicial
			if magnitud != '' and marca != '':
				flag = True
				data = grafico_marca(magnitud, marca)

	ctx = {'graficoForm' : graficoForm, 'marcas':marcas, 'flag':flag,
		'data': data,'magnitud': magnitud,}

	return render_to_response('estadisticas/grafico_marca.html', ctx, context_instance = RequestContext(request))

#Vista para manejar la informacion del grafico de marcas
def grafico_marca(magnitud, id_marca):

	i = 0
	egresos = 0
	ingresos = 0
	ganancias = 0
	total_evento = 0
	macro = []
	eventos = []
	ingresos = []
	submarcas = []
	funciones = []
	meses_egresos = []
	meses_ingresos = []
	meses_ganancias = []
	producto_evento = []
	egresos_funcion = []
	ingresos_funcion = []
	ganancias_funcion = []
	data = []
	meses = (('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), 
		('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), 
		('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), 
		('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'),)

	#Extraccion de las submarcas de una marca
	try:
		submarcas = SubMarca.objects.filter(marca=id_marca)
	except:
		error = ''

	#Verificacion del caso para ingresos
	if magnitud == 'ingresos':

		#Meses de cada magnitud
		for mes in meses:

			ingresos = 0
			#Utilizacion de cada submarca de la marca
			for submarca in submarcas:

				try:
					macros = MacroCliente.objects.filter(submarca=submarca);
				except:
					error = ''

				#Utilizacion de cada macricliente de la submarca
				for macro in macros:

					#Extraccion de datos de los eventos y funciones	
					eventos = Evento.objects.filter(macrocliente=macro)
					for evento in eventos:
						
						funciones = Funcion.objects.filter(evento=evento, dia__month=mes[0]).order_by('dia')

						#Extraccion de los ingresos de cada funcion de cada evento
						for funcion in funciones:

							#Informacion de los pedidos del evento
							try:
								producto_evento = ProductoEvento.objects.filter(evento=funcion.evento)
							except:
								error = ''
							
							#Informacion de los productos de cada evento
							for producto in producto_evento:
								productos_evento_pedido = ProductoEventoPedido.objects.filter(producto=producto)

								#Informacion de los productos pedidos en cada evento
								for producto_pedido in productos_evento_pedido:
									pedidos = Pedido.objects.filter(num_pedido=producto_pedido.num_pedido)
									
									#Informacion de los pedidos de cada evento
									for pedido in pedidos:
										ingresos += pedido.total

			#Verificacion de que existe ingreso en el mes especifico
			meses_ingresos.append((mes[1], ingresos))

		#Objeto Json que se retornara
		for item in meses_ingresos:
			data.append({'y':item[0], magnitud:str(item[1])})

	#Verificacion del caso para egresos
	elif magnitud == 'egresos':

		#Meses de cada magnitud
		for mes in meses:

			egresos = 0
			#Utilizacion de cada submarca de la marca
			for submarca in submarcas:

				try:
					macros = MacroCliente.objects.filter(submarca=submarca);
				except:
					error = ''

				#Utilizacion de cada macricliente de la submarca
				for macro in macros:

					#Extraccion de datos de los eventos y funciones	
					eventos = Evento.objects.filter(macrocliente=macro)
					for evento in eventos:

						funciones = Funcion.objects.filter(evento=evento, dia__month=mes[0]).order_by('dia')

						#Extraccion de los egresos de cada funcion de cada evento
						for funcion in funciones:

							#Informacion de los gastos o egresos de cada evento
							try:
								egresos_funcion = GastoEvento.objects.get(evento=funcion.evento, fue_pagado=True)
							except:
								error = 'Este evento no tiene egresos asociados'

							print egresos_funcion

							#Verificacion de que encontro un egreso
							if egresos_funcion != []:
								egresos += egresos_funcion.monto

			if egresos != 0:
				meses_egresos.append((mes[1], egresos))
			else:
				meses_egresos.append((mes[1], egresos))
				
		#Objeto Json que se retornara
		for item in meses_egresos:
			data.append({'y':item[0], magnitud:str(item[1])})

	#Verificacion del caso para ganancias
	elif magnitud == 'ganancias':

		#Meses de cada magnitud
		for mes in meses:

			egresos = 0
			ingresos = 0

			#Utilizacion de cada submarca de la marca
			for submarca in submarcas:

				try:
					macros = MacroCliente.objects.filter(submarca=submarca);
				except:
					error = ''

				#Utilizacion de cada macricliente de la submarca
				for macro in macros:

					#Extraccion de datos de los eventos y funciones	
					eventos = Evento.objects.filter(macrocliente=macro)
					for evento in eventos:

						funciones = Funcion.objects.filter(evento=evento, dia__month=mes[0]).order_by('dia')

						#Extraccion de los ingresos de cada funcion de cada evento
						for funcion in funciones:

							#Informacion de los pedidos del evento
							try:
								producto_evento = ProductoEvento.objects.filter(evento=funcion.evento)
							except:
								error = ''
							
							#Informacion de los productos de cada evento
							for producto in producto_evento:
								productos_evento_pedido = ProductoEventoPedido.objects.filter(producto=producto)

								#Informacion de los productos pedidos en cada evento
								for producto_pedido in productos_evento_pedido:
									pedidos = Pedido.objects.filter(num_pedido=producto_pedido.num_pedido)
									
									#Informacion de los pedidos de cada evento
									for pedido in pedidos:
										ingresos += pedido.total

							#Informacion de los gastos o egresos de cada evento
							try:
								egresos_funcion = GastoEvento.objects.get(evento=funcion.evento, fue_pagado=True)
							except:
								error = 'Este evento no tiene egresos asociados'

							#Verificacion de que encontro un egreso
							if egresos_funcion != []:
								egresos += egresos_funcion.monto

			#Verificacion de que existe ingreso en el mes especifico
			if ingresos != 0 or egresos != 0:

				meses_ganancias.append((mes[1], ingresos-egresos))
			else:
				meses_ganancias.append((mes[1], ingresos-egresos))

		#Objeto Json que se retornara
		for item in meses_ganancias:
			data.append({'y':item[0], magnitud:str(item[1])})

	#Objeto json a devolver para el grafico
	return json.dumps(data)
