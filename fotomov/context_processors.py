from staff.models import *
from tareas.models import *
from django.conf import settings
from datetime import *
import datetime

def obtener_tareas(request):
    try:
        tareas = []
        muchos_stats = []
        if request.user:
            if request.user.is_authenticated():
                us = request.user
                try:
                    hoy = date(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day)
                    usuario = Usuario.objects.get(usuario=us)
                    tareas = Tarea.objects.filter(asignado=usuario.privilegio, activa=True)
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
    except:
        pass
    return { 'tareas_menu': tareas, 'stats':muchos_stats }

def obtener_privilegio(request):
    try:
        usuario = Usuario.objects.get(usuario= request.user)
        privilegio = usuario.privilegio.valor
    except:
        privilegio = 0
    return {'privilegio_log' : privilegio}