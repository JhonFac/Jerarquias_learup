# app/models.py
from django.db import models
from django.utils import timezone


class Jerarquia(models.Model):
    jerarquia = models.CharField(max_length=255)
    area = models.CharField(max_length=20, default='')

class Empleado(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    area = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(default=timezone.now)
    estado = models.BooleanField(default=True)


class LogJerarquia(models.Model):
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    id_jerarquia = models.ForeignKey(Jerarquia, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    estado = models.BooleanField(default=True)
