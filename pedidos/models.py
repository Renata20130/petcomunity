from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from productos.models import Producto




class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    farmacia = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_farmacia', null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, default='pendiente')  # por ejemplo: pendiente, procesando, enviado

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
