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