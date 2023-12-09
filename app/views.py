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
        log_jerarquia = LogJerarquia.objects.get(id_empleado=employ.id, estado=True)

        employ_list = Empleado.objects.filter(
            logjerarquia__id_jerarquia__lt=log_jerarquia.id_jerarquia,
            logjerarquia__estado=True
        )

        for empleado in employ_list:
            logjerarquia = empleado.logjerarquia_set.first()
            print(f"ID: {empleado.id}, Nombre: {empleado.nombre}, Jerarquía: {logjerarquia.id_jerarquia.jerarquia}, ID_Jerarquía: {logjerarquia.id_jerarquia.id}, Estado: {logjerarquia.estado}")

    except Exception:
        employ = None



    print('validar jefe')

    try:
        print(employ.id)
        log_jerarquia = LogJerarquia.objects.get(id_empleado=employ.id, estado=True)
        print(log_jerarquia.id_jerarquia.id)
        jefe_jerarquia = log_jerarquia.id_jerarquia.id
        print(jefe_jerarquia)
        jefe_jerarquia_id = jefe_jerarquia + 1
        print(jefe_jerarquia_id)
        jefe = Empleado.objects.get(logjerarquia__id_jerarquia=jefe_jerarquia_id)
        print(jefe)
        nom_jefe= jefe.nombre
    except LogJerarquia.DoesNotExist:
        nom_jefe= jefe
    except Exception:
        nom_jefe= jefe

    print(employ)
    hierarchy = Jerarquia.objects.all()
    return render(request, 'details.html', {
                      'employ': employ, 
                      'nom_jefe': nom_jefe, 
                      'employ_list': employ_list, 
                      'hierarchys': hierarchy
                      }
                  )

def index(request):
    employs = Empleado.objects.all()
    return render(request, 'list_employees.html', {'employs': employs})


