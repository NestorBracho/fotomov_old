from django.forms import ModelForm
from django.db import models
from evento.models import *
from clientes.models  import *
from django import forms

class EventoForm(forms.ModelForm):
    macrocliente = forms.ModelChoiceField(queryset=MacroCliente.objects.all())
    class Meta:
        model = Evento
        exclude = ['locacion',]
