
from django.contrib.auth.decorators import login_required
from accounts.decorators import tipo_requerido
from .forms import ReservaFormCliente
from .forms import ReservaFormClinica
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import Raza
from .serializers import RazaSerializer
from rest_framework import generics


@login_required
def agendar_reserva(request):
    if request.method == 'POST':
        form = ReservaFormClinica(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user
            reserva.save()
            return redirect('home')  # o donde quieras redirigir
    else:
        form = ReservaFormClinica()
    
    return render(request, 'reservas/agendar_reserva.html', {'form': form})

@login_required
@tipo_requerido('clinica')
def registrar_reserva(request):
    if request.method == 'POST':
        form = ReservaFormClinica(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.clinica = request.user
            reserva.creada_por_clinica = True  # ¡funcionará porque ya existe ese campo!
            reserva.save()
    else:
        form = ReservaFormClinica()
    return render(request, 'reservas/registrar_reserva.html', {'form': form})


@login_required
def cliente_pedir_hora(request):
    enviado = False

    if request.method == 'POST':
        form = ReservaFormCliente(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.creada_por_clinica = False
            reserva.estado = 'pendiente'
            reserva.nombre_cliente = request.user.get_full_name() or request.user.username
            reserva.email_cliente = request.user.email or ''
            reserva.cliente = request.user  # 👈 Esta línea es esencial
            reserva.save()
            enviado = True
    else:
        form = ReservaFormCliente()

    return render(request, 'reservas/pedir_hora_cliente.html', {
        'form': form,
        'enviado': enviado
    })

def obtener_razas_por_especie(request):
    especie_seleccionada = request.GET.get('especie', '')

    if especie_seleccionada:
        # Filtra por la especie_seleccionada que viene del frontend (ej: 'perro', 'gato')
        # y selecciona solo el id y nombre para la respuesta JSON
        razas = Raza.objects.filter(especie=especie_seleccionada).values('id', 'nombre').order_by('nombre')
        data = list(razas) # Convierte el QuerySet a una lista de diccionarios
    else:
        data = [] # Si no hay especie seleccionada, devuelve una lista vacía

    return JsonResponse(data, safe=False)

@login_required
def panel_reservas_clinica(request):
    reservas = Reserva.objects.filter(clinica=request.user).order_by('-fecha', '-hora')
    print("Reservas:", reservas)  # Para debug

    return render(request, 'reservas/panel_reservas_clinica.html', {'reservas': reservas})

@login_required
def cambiar_estado_reserva(request, reserva_id, nuevo_estado):
    reserva = get_object_or_404(Reserva, id=reserva_id, clinica=request.user)
    if nuevo_estado in ['aceptada', 'rechazada']:
        reserva.estado = nuevo_estado
        reserva.save()

        asunto = f"Tu reserva ha sido {nuevo_estado.capitalize()}"
        texto_plano = f"Hola {reserva.nombre_cliente}, tu reserva para {reserva.nombre_mascota} el día {reserva.fecha} a las {reserva.hora} ha sido {nuevo_estado}."
        
        if nuevo_estado == 'aceptada':
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #2E8B57;">¡Reserva Aceptada!</h2>
                <p>Hola <strong>{reserva.nombre_cliente}</strong>,</p>
                <p>Tu reserva para <strong>{reserva.nombre_mascota}</strong> el día <strong>{reserva.fecha}</strong> a las <strong>{reserva.hora}</strong> ha sido <span style="color: green;">aceptada</span> por la clínica.</p>
                <p>¡Gracias por confiar en nosotros!</p>
                <br>
                <p style="font-size: 0.9em; color: #555;">Si tienes alguna pregunta, no dudes en contactarnos.</p>
            </body>
            </html>
            """
        else:  # rechazado
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #B22222;">Reserva Rechazada</h2>
                <p>Hola <strong>{reserva.nombre_cliente}</strong>,</p>
                <p>Lamentamos informarte que tu reserva para <strong>{reserva.nombre_mascota}</strong> el día <strong>{reserva.fecha}</strong> a las <strong>{reserva.hora}</strong> ha sido <span style="color: red;">rechazada</span> por la clínica.</p>
                <p>Por favor, contáctanos si necesitas más información.</p>
                <br>
                <p style="font-size: 0.9em; color: #555;">Gracias por tu comprensión.</p>
            </body>
            </html>
            """

        email = EmailMultiAlternatives(
            asunto,
            texto_plano,
            'tu_email@example.com',  # Cambia por tu correo configurado
            [reserva.email_cliente],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        messages.success(request, f"Reserva {nuevo_estado} correctamente y notificación enviada al cliente.")
    return redirect('panel_reservas_clinica')

class RazaListAPIView(generics.ListAPIView):
    serializer_class = RazaSerializer # Solo necesitamos el serializador aquí

    def get_queryset(self):
        """
        Este método permite filtrar las razas por el parámetro 'especie' en la URL.
        Ejemplo de URL: /api/api/razas/?especie=perro
        """
        queryset = Raza.objects.all() # Empieza con todas las razas
        
        # Obtiene el valor del parámetro 'especie' de la URL (si existe)
        especie = self.request.query_params.get('especie', None)
        
        # Si se proporcionó una especie, filtra el queryset
        if especie is not None and especie != '': # Asegúrate de que no sea None o una cadena vacía
            queryset = queryset.filter(especie=especie)
            
        return queryset
