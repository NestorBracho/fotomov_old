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
    ENVIO_CHOICES = (
        (0, 'Sin Envio'),
        (1, 'Regional'),
        (2, 'Nacional'),
        (3, 'Internacional'),
    )
    envio = forms.ChoiceField(choices=ENVIO_CHOICES)
    class Meta:
        model = Pedido
        exclude=['cliente', 'fecha', 'num_pedido', 'fecha_entrega', 'total','codigo', 'envio', 'fue_pagado',
                 'lote', 'estado', 'factura', 'direccion_entrega']
    def __init__(self, *args, **kwargs):
        super(PedidoCajaForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

class PedidoPagoForm(forms.Form):
    tipo_pago = forms.ModelChoiceField(queryset=FormaDePago.objects.all())
    monto = forms.FloatField()
    referencia = forms.CharField()