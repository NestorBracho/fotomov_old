from django.forms import ModelForm
from django.db import models
from django import forms

class ArchivoForm(forms.Form):
    archivo = forms.FileField()

class IngresarTicketForm(forms.Form):
    ticket = forms.IntegerField(label="Introduzca su numero")
    cedula = forms.IntegerField(label="Numero de cedula del cliente")

