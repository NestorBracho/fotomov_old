from django.forms import ModelForm
from django.db import models
from django import forms

class ArchivoForm(forms.Form):
    archivo = forms.FileField()