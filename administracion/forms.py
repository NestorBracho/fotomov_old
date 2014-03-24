from django.forms import ModelForm
from django.db import models
from administracion.models import *
from django import forms

class FormaDePagoForm(forms.ModelForm):
    class Meta:
        model = FormaDePago

class TipoDeGastoForm(forms.ModelForm):
    class Meta:
        model = TipoDeGasto

class GastoForm(forms.ModelForm):
    class Meta:
        model = GastoAdministracion
        exclude = ['moneda']