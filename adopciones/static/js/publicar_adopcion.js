// adopciones/static/js/publicar_adopcion.js

document.addEventListener('DOMContentLoaded', function() {

    // --- Lógica existente para la vista previa de imagen ---
    const fileInput = document.getElementById('id_imagen_fallback'); 
    console.log('fileInput encontrado:', fileInput); 

    const triggerAdditionalUploadButton = document.getElementById('triggerAdditionalUpload');
    console.log('triggerAdditionalUploadButton encontrado:', triggerAdditionalUploadButton); 

    const uploadCountSpan = document.getElementById('uploadCount');
    console.log('uploadCountSpan encontrado:', uploadCountSpan); 

    const mainImagePreview = document.getElementById('mainImagePreview');
    console.log('mainImagePreview encontrado:', mainImagePreview);

    const initialImageElement = document.querySelector('.current-image-display .preview-image');
    if (initialImageElement && mainImagePreview) {
        mainImagePreview.src = initialImageElement.src;
        mainImagePreview.style.display = 'block'; 
    } else if (mainImagePreview) {
        mainImagePreview.src = mainImagePreview.getAttribute('src'); 
        mainImagePreview.style.display = 'block';
    }

    function updateUploadCount(count) {
        if (uploadCountSpan) {
            uploadCountSpan.textContent = count + ' archivo(s)'; 
            console.log('Conteo de archivos actualizado a:', count);
        }
    }

    if (triggerAdditionalUploadButton && fileInput) {
        triggerAdditionalUploadButton.addEventListener('click', function() {
            console.log('Click en el botón "Subir Imagen" detectado.'); 
            try {
                fileInput.click();
                console.log('Intentando click() en fileInput.');
            } catch (e) {
                console.error('Error al intentar hacer click en fileInput:', e);
            }
        });
    } else {
        console.log('El botón "Subir Imagen" o el input de archivo no se encontraron para el listener.');
    }

    if (fileInput && mainImagePreview) {
        fileInput.addEventListener('change', function() {
            console.log('Evento "change" en fileInput detectado.');
            if (this.files && this.files.length > 0) {
                updateUploadCount(this.files.length);
                console.log('Archivos seleccionados:', this.files);

                const selectedFile = this.files[0];
                const reader = new FileReader();

                reader.onload = function(e) {
                    mainImagePreview.src = e.target.result;
                    mainImagePreview.style.display = 'block';
                    if (initialImageElement) {
                        initialImageElement.style.display = 'none';
                    }
                };

                reader.readAsDataURL(selectedFile);
            } else {
                updateUploadCount(0);
                mainImagePreview.src = mainImagePreview.getAttribute('src'); 
                if (initialImageElement && initialImageElement.getAttribute('src')) {
                       initialImageElement.style.display = 'block';
                }
                console.log('Ningún archivo seleccionado.');
            }
        });
    } else {
        console.log('El input de archivo o la vista previa principal no se encontraron para el listener "change".');
    }
    // --- FIN Lógica existente para la vista previa de imagen ---


    // --- COMIENZO: Lógica para cargar las razas desde la API (Dropdown en cascada) ---
    // Accede a las variables globales: Ya están definidas arriba con sus IDs correctos
    const especieSelect = document.getElementById('id_especie'); // ID por defecto de Django para el campo 'especie'
    const razaSelect = document.getElementById('razaSelect'); // ID que le diste en forms.py
    const API_RAZAS_URL = '/api/api/razas/'; // La URL a tu API de razas en Django REST
    const otrosEspecieValue = 'otro'; // Valor para "otros" en MascotaEnAdopcion.ESPECIE_CHOICES

    // Verificaciones para depurar (mantenlas por ahora si quieres)
    if (!especieSelect) {
        console.error(`Error JS: El elemento 'especieSelect' (ID: id_especie) no se encontró en el DOM.`);
        return; 
    }
    if (!razaSelect) {
        console.error(`Error JS: El elemento 'razaSelect' (ID: razaSelect) no se encontró en el DOM.`);
        return; 
    }

    function updateRazas() {
        const especieValue = especieSelect.value;
        razaSelect.innerHTML = ''; // Limpiar opciones anteriores
        razaSelect.classList.add('disabled-select');
        razaSelect.setAttribute('aria-disabled', 'true');
        razaSelect.removeAttribute('disabled');

        if (!especieValue) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Primero selecciona una especie';
            razaSelect.appendChild(option);

            razaSelect.classList.add('disabled-select');
            razaSelect.setAttribute('aria-disabled', 'true');
            razaSelect.removeAttribute('disabled');
            return;
        }

        // Usa la variable para "otros"
        if (especieValue === otrosEspecieValue) {
            const option = document.createElement('option');
            option.value = 'No Aplica'; // Guardará "No Aplica" como texto en el CharField
            option.textContent = 'No Aplica';
            razaSelect.appendChild(option);
            razaSelect.removeAttribute('disabled');
        } else {
            // Usa la URL de la API
            // El nombre del parámetro 'especie' DEBE coincidir con el que espera tu API en reservas/views.py
            fetch(`${API_RAZAS_URL}?especie=${especieValue}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.length > 0) {
                        const defaultOption = document.createElement('option');
                        defaultOption.value = '';
                        defaultOption.textContent = 'Selecciona una raza';
                        razaSelect.appendChild(defaultOption);

                        data.forEach(raza => {
                            const option = document.createElement('option');
                            // ¡IMPORTANTE! Aquí asignamos el NOMBRE de la raza al valor de la opción
                            // porque tu campo 'raza' en MascotaEnAdopcion es un CharField.
                            option.value = raza.nombre; 
                            option.textContent = raza.nombre;
                            razaSelect.appendChild(option);
                        });
                        razaSelect.removeAttribute('disabled');
                    } else {
                        const option = document.createElement('option');
                        option.value = '';
                        option.textContent = 'No hay razas disponibles';
                        razaSelect.appendChild(option);
                        razaSelect.setAttribute('disabled', 'disabled');
                    }
                })
                .catch(error => {
                    console.error('Error al cargar razas:', error);
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'Error al cargar razas';
                    razaSelect.appendChild(option);
                    razaSelect.setAttribute('disabled', 'disabled');
                });
        }
    }

    // Listener para el cambio de especie
    if (especieSelect) {
        especieSelect.addEventListener('change', updateRazas);

        // Llama a la función al cargar la página si ya hay una especie seleccionada
        if (especieSelect.value) {
            updateRazas();
        } else {
            razaSelect.innerHTML = '<option value="">Selecciona una especie primero</option>';
            razaSelect.setAttribute('disabled', 'disabled');
        }
    } 
    // --- FIN: Lógica para cargar las razas desde la API ---

    // Eliminamos la depuración del botón del widget ya que ahora no tiene un rol visual directo
    // const widgetUploadButtonLabel = document.querySelector('.custom-file-input-wrapper .upload-button');
    // if (widgetUploadButtonLabel) { console.log('Etiqueta de botón del widget encontrada:', widgetUploadButtonLabel); } else { console.log('Etiqueta de botón del widget NO encontrada.'); }
});