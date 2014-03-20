from django.forms import ModelForm
from django.db import models
from staff.models import Usuario
from tareas.models import *
from django import forms

class TareaForm(forms.Form):
    asignado = forms.ModelChoiceField(queryset=Privilegios.objects.filter(valor__lt=6))
    tarea = forms.CharField(widget=forms.Textarea)
    nombre = forms.CharField()

class CrearNotificacionFrom(forms.ModelForm):
    class Meta:
        model = Notificacion
        exclude = ['creado_fecha','fue_revisado','usuario_creador']