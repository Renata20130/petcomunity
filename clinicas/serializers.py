from rest_framework import serializers
from reservas.models import Raza

class RazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raza
        fields = ['id', 'nombre']