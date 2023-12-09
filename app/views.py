from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import EmpleadoForm
from .models import Empleado, Jerarquia, LogJerarquia
from .serializers import EmpleadoSerializer


def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save()
            jerarquia_id = request.POST.get('jerarquia')
            print(jerarquia_id)
            if jerarquia_id!='Seleccione...':
                jerarquia = Jerarquia.objects.get(id=jerarquia_id)
                LogJerarquia.objects.create(
                    id_empleado=empleado,
                    id_jerarquia=jerarquia
                )
            return redirect('/')

    form = EmpleadoForm()
    hierarchy = Jerarquia.objects.all()

    return render(request, 'crear_empleado.html', {'form': form, 'hierarchys': hierarchy})


def listar_jerarquias(request):
    hierarchy = Jerarquia.objects.all()
    return render(request, 'hierarchy_list.html', {'hierarchys': hierarchy})


def cambiar_jerarquias(request):
    if request.method == 'POST':
        hierarchy_id = request.POST.get('hierarchy')
        employ_id = request.POST.get('employ_id')
        log_jerarquia_exists = LogJerarquia.objects.filter(id_empleado=employ_id, estado=True).exists()
        if log_jerarquia_exists:
            log_jerarquia = LogJerarquia.objects.get(id_empleado=employ_id, estado=True)
            if log_jerarquia.id_jerarquia.id != int(hierarchy_id):
                employ = Empleado.objects.get(id=employ_id)
                hierarchy = Jerarquia.objects.get(id=hierarchy_id)
                LogJerarquia.objects.create(
                    id_empleado=employ,
                    id_jerarquia=hierarchy,
                    estado=True
                )
                log_jerarquia.estado = False
                log_jerarquia.save()
                return HttpResponse(f'<p class="success">Jerarquía cambiada exitosamente.</p>')
            return HttpResponse(f'<p class="warning">La jerarquía seleccionada es la misma que la actual.</p>')

        employ = Empleado.objects.get(id=employ_id)
        hierarchy = Jerarquia.objects.get(id=hierarchy_id)
        LogJerarquia.objects.create(
            id_empleado=employ,
            id_jerarquia=hierarchy,
            estado=True
        )
        return HttpResponse(f'<p class="success">Jerarquía cambiada exitosamente.</p>')




def detail_employ(request, employ_id):
    jefe="Sin Jefe"
    employ_list = []
    try:
        employ = get_object_or_404(Empleado, id=employ_id)
    except Exception: 
        employ = None

    print('validar jefe')

    try:
        log_jerarquia = LogJerarquia.objects.get(id_empleado=employ.id, estado=True)

        employ_list = Empleado.objects.filter(
            logjerarquia__id_jerarquia__lt=log_jerarquia.id_jerarquia,
            logjerarquia__estado=True
        )

        jefe_jerarquia = log_jerarquia.id_jerarquia.id + 1
        jefe = Empleado.objects.filter(logjerarquia__id_jerarquia=jefe_jerarquia, logjerarquia__estado=True).first()
        nom_jefe= jefe.nombre
    except LogJerarquia.DoesNotExist:
        nom_jefe= jefe
        employ_list= []
    except Exception:
        nom_jefe= jefe
        employ_list= []


    print(employ)
    hierarchy = Jerarquia.objects.all()
    return render(request, 'details.html', {
                      'employ': employ, 
                      'nom_jefe': nom_jefe, 
                      'employ_list': employ_list, 
                      'employ_hierarchys': log_jerarquia.id_jerarquia.jerarquia, 
                      'hierarchys': hierarchy
                      }
                  )

def index(request):
    employs = Empleado.objects.all()
    employ_details = []

    for employ in employs:
        try:
            log_jerarquia = LogJerarquia.objects.get(id_empleado=employ.id, estado=True)
            jerarquia_nombre = log_jerarquia.id_jerarquia.jerarquia
        except LogJerarquia.DoesNotExist:
            jerarquia_nombre = 'Sin Jerarquía'

        employ_details.append({
            'id': employ.id,
            'nombre': employ.nombre,
            'correo': employ.correo,
            'telefono': employ.telefono,
            'jerarquia_nombre': jerarquia_nombre,
            'estado': employ.estado,
        })

    return render(request, 'list_employees.html', {'employs': employ_details})


