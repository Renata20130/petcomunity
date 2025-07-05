from django.urls import path
from .views import lista_farmacias_con_productos

app_name = 'farmacias'

urlpatterns = [
    path('', lista_farmacias_con_productos, name='lista_farmacias'),
]