#encoding:utf-8
from django.forms import ModelForm
from django import forms
from staff.models import Usuario, Notificacion

class RegisUsuarioForm(forms.Form):
    privilegios_choices = (
      ('1','Administrador'),
      ('2','Logistica'),
      ('3','Edición'),
      ('4','Comunicación'),
      ('5','Gerencia'),
    )
    nombre = forms.CharField()
    apellido = forms.CharField()
    cedula = forms.CharField()
    privilegio = forms.ChoiceField(choices=privilegios_choices, label='Tipos de usuario')

class RegisNotificacion(forms.Form):
    categoria = forms.CharField(widget=forms.Textarea)
    mensaje = forms.CharField(widget=forms.Textarea)
    fecha_creado = forms.DateField()
    hora = forms.DateTimeField()
    realizado = forms.BooleanField(widget=forms.CheckboxInput)
    fecha_asignacion = forms.DateField()


