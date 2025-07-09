document.addEventListener('DOMContentLoaded', function() {
    console.log("panel_clinica.js se está ejecutando!"); 

    // --- COMIENZO DEL CÓDIGO A ELIMINAR/REEMPLAZAR ---
    // ELIMINA O COMENTA ESTE BLOQUE COMPLETO, ESTÁ DUPLICADO Y ES INCORRECTO
    /*
    document.querySelectorAll('.switch input[type="checkbox"]').forEach(switchEl => {
        switchEl.addEventListener('change', function() {
            const id = this.dataset.id;
            const csrfToken = '{{ csrf_token }}'; // INCORRECTO AQUÍ
            fetch("{% url 'cambiar_estado_mascota' %}", { // INCORRECTO AQUÍ
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded', // INCORRECTO
                    'X-CSRFToken': csrfToken
                },
                body: `id=${id}`
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert('Error al cambiar estado');
                    this.checked = !this.checked;
                }
            });
        });
    });
    */
    // --- FIN DEL CÓDIGO A ELIMINAR/REEMPLAZAR ---


    // Función para confirmar eliminación (esta es correcta y la puedes mantener)
    function confirmarEliminacion() {
        return confirm("¿Seguro que quieres eliminar esta publicación?");
    }

    // === Lógica para el switch de estado (ESTE ES EL BLOQUE CORRECTO) ===
    const switchesEstado = document.querySelectorAll('.estado-switch-container input[type="checkbox"]');

    switchesEstado.forEach(switchElement => {
        switchElement.addEventListener('change', function() {
            const mascotaId = this.dataset.id;
            const nuevoEstado = this.checked ? 'publicada' : 'pendiente';

            console.log(`Intentando cambiar mascota ${mascotaId} a estado: ${nuevoEstado}`);

            // Obtener el token CSRF de forma segura desde el DOM
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch('/adopciones/cambiar_estado/', { // URL HARDCODEADA, PERO SEGURA SI ES FIJA
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // ¡CORRECTO!
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ // ¡CORRECTO!
                    mascota_id: mascotaId,
                    estado: nuevoEstado
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la solicitud: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log('Estado de la mascota actualizado con éxito:', data.message);
                    
                    // Lógica para ocultar/mostrar la tarjeta
                    const mascotaCard = document.getElementById(`mascota-${mascotaId}`);
                    if (mascotaCard) {
                        if (nuevoEstado === 'pendiente') {
                            mascotaCard.style.display = 'none'; 
                        } else {
                            mascotaCard.style.display = 'block'; 
                        }
                    }
                } else {
                    console.error('Error al actualizar estado:', data.message);
                    this.checked = !this.checked;
                    alert('Hubo un error al actualizar el estado: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error de red o del servidor:', error);
                this.checked = !this.checked;
                alert('No se pudo conectar con el servidor para actualizar el estado.');
            });
        });
    });

    // Asegúrate de que cualquier otro JavaScript esté aquí dentro del DOMContentLoaded

}); // Fin de DOMContentLoaded