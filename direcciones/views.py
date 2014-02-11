from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from direcciones import *

def nueva_direccion(request):
    if request.method == 'POST':
        pass
    else:
        pass
    return render_to_response('staff/nueva_direccion.html', {}, context_instance= RequestContext(request))