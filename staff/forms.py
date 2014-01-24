#encoding:utf-8
from django.forms import ModelForm, PasswordInput
from django import forms
from staff.models import *
from django.contrib.auth.models import User

class RegisUsuarioForm(forms.Form):
    nombre = forms.CharField()
    apellido = forms.CharField()
    cedula = forms.CharField()
    email = forms.EmailField()
    privilegio = forms.ModelChoiceField(queryset=Privilegios.objects.all())

class RegisNotificacion(forms.Form):
    categoria = forms.CharField(widget=forms.Textarea)
    mensaje = forms.CharField(widget=forms.Textarea)
    fecha_creado = forms.DateField()
    hora = forms.DateTimeField()
    realizado = forms.BooleanField(widget=forms.CheckboxInput)
    fecha_asignacion = forms.DateField()
