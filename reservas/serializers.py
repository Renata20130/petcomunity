# reservas/serializers.py
from rest_framework import serializers
from .models import Raza

class RazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raza
        fields = ['id', 'nombre', 'especie'] # Estos son los campos que tu API devolverá