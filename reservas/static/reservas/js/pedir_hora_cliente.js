// reservas/static/reservas/js/pedir_hora_cliente.js

document.addEventListener('DOMContentLoaded', function() {
    // Accede a las variables globales definidas en el HTML
    const especieSelect = document.getElementById(ESPECIE_SELECT_ID);
    const razaSelect = document.getElementById(RAZA_SELECT_ID);
    const API_RAZAS_URL = '/api/api/razas/';
    const otrosEspecieValue = OTROS_ESPECIE_VALUE; // El valor para "otros"

    // Verificaciones para depurar (mantenlas por ahora)
    if (!especieSelect) { 
        console.error(`Error JS: El elemento 'especieSelect' (ID: ${ESPECIE_SELECT_ID}) no se encontró en el DOM.`);
        return; // Salir para evitar el error
    }
    if (!razaSelect) {
        console.error(`Error JS: El elemento 'razaSelect' (ID: ${RAZA_SELECT_ID}) no se encontró en el DOM.`);
        return; // Salir para evitar el error
    }

    function updateRazas() {
        const especieValue = especieSelect.value;
        razaSelect.innerHTML = ''; // Limpiar opciones anteriores
        razaSelect.setAttribute('disabled', 'disabled'); // Deshabilitar raza por defecto
        
        if (!especieValue) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Primero selecciona una especie';
            razaSelect.appendChild(option);
            return;
        }

        // Usa la variable para "otros"
        if (especieValue === otrosEspecieValue) {
            const option = document.createElement('option');
            option.value = 'no_aplica';
            option.textContent = 'No Aplica';
            razaSelect.appendChild(option);
            razaSelect.removeAttribute('disabled');
        } else {
            // Usa la URL de la API
            fetch(`${API_RAZAS_URL}?especie=${especieValue}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.length > 0) {
                        data.forEach(raza => {
                            const option = document.createElement('option');
                            option.value = raza.id;
                            option.textContent = raza.nombre;
                            razaSelect.appendChild(option);
                        });
                        razaSelect.removeAttribute('disabled');
                    } else {
                        const option = document.createElement('option');
                        option.value = '';
                        option.textContent = 'No hay razas disponibles';
                        razaSelect.appendChild(option);
                    }
                })
                .catch(error => {
                    console.error('Error al cargar razas:', error);
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'Error al cargar razas';
                    razaSelect.appendChild(option);
                });
        }
    }

    especieSelect.addEventListener('change', updateRazas);
    if (especieSelect.value) {
        updateRazas();
    }
});