from django.forms import ModelForm
from django.db import models
from evento.models import *
from clientes.models  import *
from django import forms

class EventoForm(forms.ModelForm):
    macrocliente = forms.ModelChoiceField(queryset=MacroCliente.objects.all())
    encargado = forms.ChoiceField()
    class Meta:
        model = Evento