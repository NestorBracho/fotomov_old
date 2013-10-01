#encoding:utf-8
import datetime
from django.forms import ModelForm
from django.db import models 
from django import forms
from django.contrib.auth.models import User
from manager.models import *
from django.contrib.admin.widgets import AdminDateWidget 
from django.forms.extras.widgets import SelectDateWidget

class PedidoForm(forms.Form):
  top = datetime.datetime.today().year
  marca_choices = (
    ('Toyota', 'Toyota'),
    ('Ford', 'Ford'),
    ('Jeep', 'Jeep'),
    ('Nisan', 'Nisan'),
    )
  operador_choices = (
    ('0414', '0414'),
    ('0424', '0424'),
    ('0412', '0412'),
    ('0416', '0416'),
    ('0426', '0426'),
    )
  choices=((str(x), x) for x in range(1980,int(top)+1))
  marca = forms.ChoiceField(choices=marca_choices)
  modelo = forms.CharField()
  year = forms.ChoiceField(choices,label='Año')
  serial = forms.CharField(required=False)
  version = forms.CharField(required=False)
  user_email = forms.EmailField()
  user_pass = forms.CharField()
  user_pass2 = forms.CharField()
  user_nombre = forms.CharField()
  user_apellido = forms.CharField()
  user_telfop = forms.ChoiceField(choices=operador_choices)
  user_telf = forms.CharField(max_length=7,min_length=7)

class DatosClientForm(forms.Form):
  operador_choices = (
    ('0414', '0414'),
    ('0424', '0424'),
    ('0412', '0412'),
    ('0416', '0416'),
    ('0426', '0426'),
    )
  nombre = forms.CharField()
  apellido = forms.CharField()
  clave = forms.CharField(widget=forms.PasswordInput)
  clave_confirmacion = forms.CharField(widget=forms.PasswordInput)
  cod_telefono = forms.ChoiceField(choices=operador_choices,required=False)
  telefono = forms.CharField(max_length=7,min_length=7,required=False)
  email = forms.EmailField(required=False)

  
