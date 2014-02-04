from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from evento.forms import *
from evento.models import *

def nuevo_evento(request):
    gastos_predeterminados = Gasto.objects.filter(predeterminado = True)
    if request.method == 'POST':
        pass
    else:
        formulario = EventoForm()
    return render_to_response('evento/nuevo_evento.html', {'formulario': formulario, 'gastos': gastos_predeterminados}, context_instance = RequestContext(request))