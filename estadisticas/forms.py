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

	ano = forms.ChoiceField(choices=choices, required=False)

#Formulario de filtrado de staff
class StaffForm(forms.Form):

	privilegios = Privilegios.objects.all()
	choices = []
	choices.append(('','- Staff -'))

	for privilegio in privilegios:
		choices.append((privilegio.nombre,privilegio.nombre),)

	privilegios = forms.ChoiceField(choices=choices, required=False)

# Formulario para generar graficos
class GraficoForm(forms.Form):
	choicesM = (('','- magnitud -'), ('ingreso','Ingreso'),('egreso','Egreso'),
	('ganancia','Ganancia'),('cantidad','Cantidad'),)

	choicesC = (('','- categoria -'), ('marca','Marca'),('submarca','Submarca'),
	('macro','Macroclientes'),)
	
	choicesR = (('','- registro -'), ('0',''))

	magnitud = forms.ChoiceField(choices=choicesM, required=False)

	categoria = forms.ChoiceField(choices=choicesC, required=False, widget=forms.Select(attrs={'disabled':'true'}))

	registro = forms.ChoiceField(choices=choicesR, required=False, widget=forms.Select(attrs={'disabled':'true'}))

