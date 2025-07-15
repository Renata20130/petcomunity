document.addEventListener('DOMContentLoaded', () => {
    const API_RAZAS_URL = '/clinicas/api/razas/'; 
    const especieSelect = document.getElementById('id_especie');
    const razaSelect = document.getElementById('id_raza');

    especieSelect.addEventListener('change', () => {
        const especieValue = especieSelect.value;

        razaSelect.innerHTML = '';
        razaSelect.disabled = true;

        if (!especieValue) {
            razaSelect.innerHTML = '<option value="">Primero selecciona especie</option>';
            return;
        }

        fetch(`${API_RAZAS_URL}?especie=${especieValue}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.json();
            })
            .then(data => {
                if (data.length > 0) {
                    const defaultOption = document.createElement('option');
                    defaultOption.value = '';
                    defaultOption.textContent = '-- Selecciona una raza --';
                    razaSelect.appendChild(defaultOption);

                    data.forEach(raza => {
                        const option = document.createElement('option');
                        option.value = raza.id;
                        option.textContent = raza.nombre;
                        razaSelect.appendChild(option);
                    });
                    razaSelect.disabled = false;
                } else {
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'No hay razas disponibles';
                    razaSelect.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Error al cargar razas:', error);
                razaSelect.innerHTML = '<option value="">Error al cargar razas</option>';
            });
    });
});
