from django.forms import ModelForm
from django.db import models
from estadisticas.models import *
from staff.models import *
from django import forms
import datetime

#Formulario del filro de meses de estadisticas
class MesesForm(forms.Form):

	meses = (('','- Mes -'),('1','Enero'),('2','Febrero'),
		('3','Marzo'),('4','Abril'),('5','Mayo'),
		('6','Junio'),('7','Julio'),('8','Agosto'),
		('9','Septiembre'),('10','Octubre'),
		('11','Noviembre'),('12','Diciembre'),)

	mes = forms.ChoiceField(choices=meses, required=False)

#Formulario del filro de anios de estadisticas
class AnosForm(forms.Form):

	anio_inicial = 2013
	fecha_actual = datetime.datetime.now()
	anios = range(anio_inicial, int(fecha_actual.year+1))
	choices = []

	choices.append(('','- Ano -'))
	for ano in anios:
		choices.append((ano,ano),)

	ano = forms.ChoiceField(choices=choices)

#Formulario de filtrado de staff
class StaffForm(forms.Form):

	privilegios = Privilegios.objects.all()
	choices = []
	choices.append(('','- Staff -'))

	for privilegio in privilegios:
		choices.append((privilegio.nombre,privilegio.nombre),)

	privilegios = forms.ChoiceField(choices=choices, required=False)

#Formulario de magnitudes de busqueda del grafico de estadisticas
class MagnitudForm(forms.Form):

	choices = (('','- magnitud -'), ('ingreso','Ingreso'),('egreso','Egreso'),
	('ganancia','Ganancia'),('cantidad','Cantidad'),)

	magnitud = forms.ChoiceField(choices=choices, required=False)

#Formulario de categorias de busqueda del grafico de estadisticas
class CategoriasForm(forms.Form):

	choices = (('','- categoria -'), ('marca','Marca'),('submarca','Submarca'),
	('macro','Macroclientes'),)

	categoria = forms.ChoiceField(choices=choices, required=False)

#Formulario de registros de busqueda del grafico de estadisticas
class RegistroForm(forms.Form):

	choices = (('','- registro -'), ('',''))

	registro = forms.ChoiceField(choices=choices, required=False, widget=forms.Select(attrs={'disabled':'true'}))