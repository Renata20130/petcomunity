document.addEventListener('DOMContentLoaded', function() {
    const switches = document.querySelectorAll('.estado-switch-container input[type="checkbox"]');

    // Asegúrate de que el token CSRF esté disponible
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    switches.forEach(function(s) {
        s.addEventListener('change', function() {
            const mascotaId = this.dataset.id;
            const nuevoEstado = this.checked ? 'publicada' : 'pendiente';
            const csrftoken = getCookie('csrftoken');
            const tarjetaMascota = document.getElementById(`mascota-${mascotaId}`); // <-- Obtiene la referencia a la tarjeta

            fetch(`/mascotas/${mascotaId}/actualizar_estado/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ estado: nuevoEstado })
            })
            .then(response => {
                // Verifica si la respuesta es válida antes de parsearla
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.error || `Error del servidor: ${response.status}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log('Estado actualizado exitosamente:', data.estado_actual);

                    // Lógica para OCULTAR o MOSTRAR la tarjeta completa
                    if (data.estado_actual === 'pendiente' || data.estado_actual === 'adoptada') {
                        if (tarjetaMascota) {
                            tarjetaMascota.style.display = 'none'; // ¡Aquí se oculta!
                            console.log(`Mascota ${mascotaId} oculta (estado: ${data.estado_actual}).`);
                        }
                    } else { // Si el estado es 'publicada'
                        if (tarjetaMascota) {
                            tarjetaMascota.style.display = 'block'; // O 'flex', 'grid', etc., según tu CSS original
                            console.log(`Mascota ${mascotaId} visible (estado: ${data.estado_actual}).`);
                        }
                    }

                    // Actualiza el texto del estado en la tarjeta (esto ya lo tienes)
                    const estadoTextElement = this.closest('.estado-switch-container').querySelector('p strong');
                    if (estadoTextElement) {
                        estadoTextElement.textContent = 'Estado: ' + data.estado_actual.charAt(0).toUpperCase() + data.estado_actual.slice(1);
                    }
                } else {
                    alert('Error: ' + data.error);
                    this.checked = !this.checked; // Revertir el switch
                }
            })
            .catch(error => {
                console.error('Hubo un error con la solicitud fetch:', error);
                alert('No se pudo actualizar el estado. Por favor, intenta de nuevo.');
                this.checked = !this.checked; // Revertir el switch
            });
        });
    });
});