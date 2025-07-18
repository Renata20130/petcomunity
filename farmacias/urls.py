from django.urls import path
from .views import lista_farmacias_con_productos
from . import views
from .views import buscar_farmacias


app_name = 'farmacias'

urlpatterns = [
    path('', lista_farmacias_con_productos, name='lista_farmacias'),
    path('buscar/', buscar_farmacias, name='buscar_farmacias'),



]