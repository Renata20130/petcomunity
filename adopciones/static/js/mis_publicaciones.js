document.addEventListener('DOMContentLoaded', function() {
    const switches = document.querySelectorAll('.estado-switch-container input[type="checkbox"]');

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
            const checkbox = this;
            const mascotaId = checkbox.dataset.id;
            const nuevoEstado = checkbox.checked ? 'publicada' : 'pendiente';
            const csrftoken = getCookie('csrftoken');
            const tarjetaMascota = document.getElementById(`mascota-${mascotaId}`);

            fetch(`/mascotas/${mascotaId}/actualizar_estado/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ estado: nuevoEstado })
            })
            .then(response => {
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

                    if (data.estado_actual === 'pendiente' || data.estado_actual === 'adoptada') {
                        if (tarjetaMascota) {
                            tarjetaMascota.style.display = 'none';
                            console.log(`Mascota ${mascotaId} oculta (estado: ${data.estado_actual}).`);
                        }
                    } else if (data.estado_actual === 'publicada') {
                        if (tarjetaMascota) {
                            // Ajusta según el display original, ej: 'flex'
                            tarjetaMascota.style.display = 'block';
                            console.log(`Mascota ${mascotaId} visible (estado: ${data.estado_actual}).`);
                        }
                    }

                    // Actualizar texto del estado (asegúrate que el selector coincida con tu HTML)
                    const estadoTextElement = tarjetaMascota.querySelector('.estado-switch-container p strong');
                    if (estadoTextElement) {
                        estadoTextElement.textContent = 'Estado: ' + data.estado_actual.charAt(0).toUpperCase() + data.estado_actual.slice(1);
                    }
                } else {
                    alert('Error: ' + data.error);
                    checkbox.checked = !checkbox.checked;
                }
            })
            .catch(error => {
                console.error('Error en fetch:', error);
                alert('No se pudo actualizar el estado. Por favor, intenta de nuevo.');
                checkbox.checked = !checkbox.checked;
            });
        });
    });
});
