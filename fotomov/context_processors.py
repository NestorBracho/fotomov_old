from staff.models import *
from tareas.models import *
from django.conf import settings
from datetime import *
import datetime

def obtener_tareas(request):
    print settings.MEDIA_ROOT
    if request.user:
        if request.user.is_authenticated():
            us = request.user
            try:
                hoy = date(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day)
                usuario = Usuario.objects.get(usuario=us)
                tareas = Tarea.objects.filter(asignado=usuario.privilegio, activa=True)
                muchos_stats = []
                for tarea in tareas:
                    if tarea.fecha == hoy:
                        aux = '2-'+str(tarea.id)
                        muchos_stats.append(aux)    #la tarea es hoy!
                    elif hoy + datetime.timedelta(days = 1) == tarea.fecha:
                        aux = '1-'+str(tarea.id)
                        muchos_stats.append(aux)    #la tarea es maniana!
                    elif tarea.fecha < hoy:
                        aux = '3-'+str(tarea.id)
                        muchos_stats.append(aux)    #la tarea esta vencida
                    else:
                        aux = '0-'+str(tarea.id)
                        muchos_stats.append(aux)    #no hay rollo
            except:
                pass
    return { 'tareas_menu': tareas, 'stats':muchos_stats }