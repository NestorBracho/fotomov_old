from staff.models import *
from tareas.models import *
from django.conf import settings

def obtener_tareas(request):
    print settings.MEDIA_ROOT
    tareas = ""
    if request.user:
        if request.user.is_authenticated():
            us = request.user
            try:
                usuario = Usuario.objects.get(usuario=us)
                tareas = Tarea.objects.filter(asignado=usuario.privilegio, activa=True)
            except:
                pass
    return { 'tareas': tareas }