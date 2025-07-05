from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.
from django.shortcuts import render
from .models import Farmacia

def lista_farmacias_con_productos(request):
    # Filtra solo usuarios que sean farmacias. Asumo que tienes perfil con tipo:
    farmacias = User.objects.filter(profile__tipo='farmacia').prefetch_related('productos')

    context = {
        'farmacias': farmacias,
    }
    return render(request, 'farmacias/lista_farmacias.html', context)







