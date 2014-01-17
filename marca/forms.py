from django.forms import ModelForm
from django.db import models
from marca.models import *
from django import forms

class MarcaForm(forms.Form):
    nombre = forms.CharField()

class SubMarcaForm(forms.Form):
    nombre = forms.CharField()

class EditarSubMarcaForm(forms.Form):
    marca = forms.ModelChoiceField(queryset= Marca.objects.all())
    nombre = forms.CharField()
