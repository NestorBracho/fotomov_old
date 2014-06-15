#encoding:utf-8
from django.forms import ModelForm, PasswordInput
from django import forms
from staff.models import *
from django.contrib.auth.models import User

class RegisUsuarioForm(forms.Form):
    nombre = forms.CharField(required=False)
    apellido = forms.CharField(required=False)
    cedula = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    privilegio = forms.ModelChoiceField(queryset=Privilegios.objects.all())

class EditarUsuarioForm(forms.Form):
    nombre = forms.CharField(required=False)
    apellido = forms.CharField(required=False)
    cedula = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    telefono_fijo = forms.CharField(required=False)
    telefono_celular = forms.CharField(required=False)
    telefono_otro = forms.CharField(required=False)
    twitter = forms.CharField(required=False)

class EquiposForm(forms.ModelForm):
    class Meta:
        model = Equipos

class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia

class DatoDePagoForm(forms.ModelForm):
    class Meta:
        model = DatoDePago

class RegisStaffForm(forms.Form):
    nombre = forms.CharField()
    apellido = forms.CharField()
    cedula = forms.CharField()
    email = forms.EmailField()
    equipos = forms.CharField(widget=forms.Textarea)

class RegisNotificacion(forms.Form):
    categoria = forms.CharField(widget=forms.Textarea)
    mensaje = forms.CharField(widget=forms.Textarea)
    fecha_creado = forms.DateField()
    hora = forms.DateTimeField()
    realizado = forms.BooleanField(widget=forms.CheckboxInput)
    fecha_asignacion = forms.DateField()

class PrivilegioFrom(forms.Form):
    nombre = forms.CharField(max_length=60)

class ArchivoAdjuntoStaff(forms.ModelForm):
    class Meta:
        model = ArchivoAdjunto
        exclude = ['cliente', 'tipo_staff']