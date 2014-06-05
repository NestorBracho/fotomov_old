from django.forms import ModelForm
from django.db import models
from productos.models import *
from django import forms

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        exclude=['cliente', 'fecha', 'num_pedido', 'fecha_entrega', 'total','codigo', 'envio', 'fue_pagado',
                 'lote', 'estado', 'factura']

class PedidoCajaForm(forms.ModelForm):
    envio = forms.ChoiceField(choices=TipoEnvio.objects.all().values_list('id', 'tipo'))
    class Meta:
        model = Pedido
        exclude=['cliente', 'fecha', 'num_pedido', 'fecha_entrega', 'total','codigo', 'envio', 'fue_pagado',
                 'lote', 'estado', 'factura', 'direccion_entrega']
    def __init__(self, *args, **kwargs):
        super(PedidoCajaForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

class PedidoPagoForm(forms.Form):
    tipos = FormaDePago.objects.all()

    CHOICES = ()
    for tipo in tipos:
        tupla = ((tipo.id, tipo.nombre),)
        CHOICES = CHOICES + tupla
    tipo_pago = forms.ChoiceField(choices=CHOICES)
    referencia = forms.CharField()
    monto = forms.FloatField(widget=forms.TextInput(attrs={'onkeypress':'return numero_float(event)'}))