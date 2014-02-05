from django.forms import ModelForm
from django.db import models
from clientes.models import *
from marca.models import *
from django import forms

class MacroClienteForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=Marca.objects.all())
    class Meta:
        model = MacroCliente

class MacroClienteContactoForm(forms.ModelForm):
    class Meta:
        model = Encargado
        exclude = ['macrocliente']