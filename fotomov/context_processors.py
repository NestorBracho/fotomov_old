from staff.models import *
from tareas.models import *

def obtener_tareas(request):
    if request.user:
        if request.user.is_authenticated():
            us = request.user
            usuario = Usuario.objects.get(usuario=us)
            tareas = Tarea.objects.filter(asignado=usuario.privilegio)
    return { 'tareas': tareas }