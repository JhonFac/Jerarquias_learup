# app/serializers.py
from rest_framework import serializers

from .models import Empleado, Jerarquia, LogJerarquia


class JerarquiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jerarquia
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    jerarquia = JerarquiaSerializer()

    class Meta:
        model = Empleado
        fields = '__all__'

class LogJerarquiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogJerarquia
        fields = '__all__'
