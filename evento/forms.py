from django.forms import ModelForm
from django.db import models
from evento.models import *
from clientes.models  import *
from productos.models import Items, ItemsPrestado
from django import forms
from marca.models import Marca

class EventoForm(forms.ModelForm):
    marcas = forms.ModelChoiceField(queryset=Marca.objects.all(), required=False)
    macrocliente = forms.ModelChoiceField(queryset=MacroCliente.objects.all().exclude(id=1))
    tipo = forms.ModelChoiceField(queryset=Tipos_Eventos.objects.all().exclude(id=1))
    class Meta:
        model = Evento
        exclude = ['locacion', 'encargado', 'sede', 'cliente']

class TiposEventoForm(forms.ModelForm):
    class Meta:
        model = Tipos_Eventos

class PautaForm(forms.Form):
    nombre = forms.CharField(max_length=300)
    pauta = forms.CharField(max_length=2000, widget=forms.Textarea)

class BloqueForm(forms.ModelForm):
    class Meta:
        model = Bloque

class CorreoForm(forms.Form):

    evento = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'type': 'hidden', 'id':'evento'}))
    funcion = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'type': 'hidden', 'id':'funcion'}))
    staff = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'type': 'hidden', 'id':'staff'}))

class NuevoItemForm(forms.ModelForm):
    class Meta:
        model = Items
