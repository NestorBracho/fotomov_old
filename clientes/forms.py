from django.forms import ModelForm
from django.db import models
from clientes.models import *
from marca.models import *
from django import forms

class MacroClienteForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=Marca.objects.all())
    class Meta:
        model = MacroCliente

class MacroClienteContactoForm(forms.Form):
    nombreContacto = forms.CharField(max_length=200, label='Nombre completo')
    cedula = forms.CharField(max_length=8)
    cargo = forms.CharField(max_length=30)
    telefono = forms.CharField(max_length=11)
    email = forms.EmailField()
    descripcion = forms.CharField(widget=forms.Textarea,max_length=500, required=False)