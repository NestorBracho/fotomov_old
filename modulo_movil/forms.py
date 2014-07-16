from django.forms import ModelForm
from django.db import models
from django import forms
from modulo_movil.models import *
from productos.models import *

class ArchivoForm(forms.Form):
    archivo = forms.FileField()

class IngresarTicketForm(forms.Form):
    ticket = forms.IntegerField(label="Introduzca numero de pedido")
    cedula = forms.IntegerField(label="Numero de cedula del cliente")

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido

class PedidoReducidoForm(PedidoForm):
    class Meta(PedidoForm.Meta):
        exclude = ('evento', 'cliente', 'num_pedido', 'total', 'codigo', 'lote', 'descuento')
