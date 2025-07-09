
document.addEventListener('DOMContentLoaded', function() {

        const fileInput = document.getElementById('id_imagen_fallback'); 
        console.log('fileInput encontrado:', fileInput); 
     
    
        const triggerAdditionalUploadButton = document.getElementById('triggerAdditionalUpload');
        console.log('triggerAdditionalUploadButton encontrado:', triggerAdditionalUploadButton); 

        const uploadCountSpan = document.getElementById('uploadCount');
        console.log('uploadCountSpan encontrado:', uploadCountSpan); 

        const mainImagePreview = document.getElementById('mainImagePreview');
        console.log('mainImagePreview encontrado:', mainImagePreview);

        const razaSelect = document.getElementById('razaSelect'); 
        const especieSelect = document.getElementById('id_especie'); // ID por defecto de Django para el campo 'especie'


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
                uploadCountSpan.textContent = count + ' archivo(s)'; // Actualiza el texto para que diga "X archivo(s)"
                console.log('Conteo de archivos actualizado a:', count);
            }
        }

        if (triggerAdditionalUploadButton && fileInput) {
            triggerAdditionalUploadButton.addEventListener('click', function() {
                console.log('Click en el botón "Subir Imagen" detectado.'); // Cambiado el mensaje de log
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
                        // Oculta la imagen del widget si existe, para evitar duplicación visual
                        if (initialImageElement) {
                            initialImageElement.style.display = 'none';
                        }
                    };

                    reader.readAsDataURL(selectedFile);
                } else {
                    updateUploadCount(0);
                    mainImagePreview.src = mainImagePreview.getAttribute('src'); 
                    // Muestra la imagen del widget si estaba oculta y había una imagen inicial
                    if (initialImageElement && initialImageElement.getAttribute('src')) {
                         initialImageElement.style.display = 'block';
                    }
                    console.log('Ningún archivo seleccionado.');
                }
            });
        } else {
            console.log('El input de archivo o la vista previa principal no se encontraron para el listener "change".');
        }

        // === Lógica para cargar las razas desde la API (Dropdown en cascada) ===
    function fetchAndPopulateRazas(selectedEspecieValue) {
        // Si no se ha seleccionado ninguna especie, vacía y deshabilita el select de raza
        if (!selectedEspecieValue) {
            razaSelect.innerHTML = '<option value="">Selecciona una especie primero</option>';
            razaSelect.disabled = true;
            return;
        }

        // Construye la URL de la API con el parámetro de especie
        // La URL es '/api/razas_por_especie/' y espera un parámetro 'especie'
        const apiEndpoint = `/api/razas_por_especie/?especie=${encodeURIComponent(selectedEspecieValue)}`;

        razaSelect.innerHTML = '<option value="">Cargando razas...</option>'; // Mensaje de carga
        razaSelect.disabled = true; // Deshabilita mientras carga

        fetch(apiEndpoint)
            .then(response => {
                if (!response.ok) {
                    // Lanza un error si la respuesta no es OK (ej. 404, 500)
                    throw new Error(`Error HTTP! Estado: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                razaSelect.innerHTML = '<option value="">Selecciona una raza</option>'; // Opción por defecto
                razaSelect.disabled = false;

                // Asumiendo que 'data' es un array de objetos como:
                // [{"id": 1, "nombre": "Labrador"}, {"id": 2, "nombre": "Poodle"}]
                // O un array de strings: ["Labrador", "Poodle"]
                if (Array.isArray(data)) {
                    data.forEach(item => {
                        const option = document.createElement('option');
                        // Si el item es un objeto con id y nombre (ideal para guardar ID en DB)
                        if (typeof item === 'object' && item !== null && 'id' in item && 'nombre' in item) {
                            option.value = item.nombre;
                            option.textContent = item.nombre;
                        } else { // Si el item es directamente el nombre de la raza (string)
                            option.value = item;
                            option.textContent = item;
                        }
                        razaSelect.appendChild(option);
                    });
                }
                console.log(`Razas cargadas exitosamente para ${selectedEspecieValue}:`, data);
            })
            .catch(error => {
                console.error(`Error al cargar las razas para ${selectedEspecieValue}:`, error);
                razaSelect.innerHTML = '<option value="">Error al cargar razas</option>';
                razaSelect.disabled = true; // Mantén deshabilitado en caso de error
            });
    }

    // Listener para cuando cambia la especie
    if (especieSelect) {
        especieSelect.addEventListener('change', function() {
            const selectedEspecieValue = this.value;
            fetchAndPopulateRazas(selectedEspecieValue);
        });

        // Llama a la función al cargar la página si ya hay una especie seleccionada
        // Esto es útil si estás editando una mascota existente y ya tiene una especie preseleccionada
        if (especieSelect.value) {
            fetchAndPopulateRazas(especieSelect.value);
        } else {
            // Si no hay especie seleccionada al cargar, deshabilita el select de raza y muestra mensaje
            razaSelect.innerHTML = '<option value="">Selecciona una especie primero</option>';
            razaSelect.disabled = true;
        }
    } else {
        console.error('Elemento select de Especie (ID: id_especie) no encontrado.');
    }
        // Eliminamos la depuración del botón del widget ya que ahora no tiene un rol visual directo
        // const widgetUploadButtonLabel = document.querySelector('.custom-file-input-wrapper .upload-button');
        // if (widgetUploadButtonLabel) { console.log('Etiqueta de botón del widget encontrada:', widgetUploadButtonLabel); } else { console.log('Etiqueta de botón del widget NO encontrada.'); }
    });