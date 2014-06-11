from django.forms import ModelForm
from django.db import models
from clientes.models import *
from marca.models import *
from django import forms

class MacroClienteForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=Marca.objects.all().exclude(id=1))
    class Meta:
        model = MacroCliente

class MacroClienteContactoForm(forms.Form):
    nombreContacto = forms.CharField(max_length=200, label='Nombre completo')
    cedula = forms.CharField(max_length=8, required=False)
    cargo = forms.CharField(max_length=30)
    telefono = forms.CharField(max_length=40)
    email = forms.EmailField()
    descripcion_contacto = forms.CharField(widget=forms.Textarea,max_length=500, required=False)

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
