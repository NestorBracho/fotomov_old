from django.forms import ModelForm
from django.db import models
from evento.models import *
from clientes.models  import *
from django import forms

class EventoForm(forms.ModelForm):
    macrocliente = forms.ModelChoiceField(queryset=MacroCliente.objects.all())
    class Meta:
        model = Evento
        exclude = ['locacion', 'encargado', 'sede', 'fecha_entrega']

class TiposEventoForm(forms.ModelForm):
    class Meta:
        model = Tipos_Eventos

class PautaForm(forms.Form):
    nombre = forms.CharField(max_length=300)
    pauta = forms.CharField(max_length=2000, widget=forms.Textarea)

class BloqueForm(forms.ModelForm):
    class Meta:
        model = Bloque
