from django.forms import ModelForm
from django.db import models
from clientes.models import *
from django import forms

class MacroClienteForm(forms.ModelForm):
    class Meta:
        model = MacroCliente
