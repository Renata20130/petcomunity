document.addEventListener('DOMContentLoaded', function() {
    const tarjetasMascota = document.querySelectorAll('.tarjeta-mascota');
    const panelDetalles = document.getElementById('panelDetallesMascota');
    const cerrarPanelBtn = document.querySelector('.cerrar-panel');

    // Elementos dentro del panel para rellenar
    const panelImagen = document.getElementById('panel-imagen');
    const panelNombre = document.getElementById('panel-nombre');
    const panelEspecie = document.getElementById('panel-especie');
    const panelRaza = document.getElementById('panel-raza'); 
    const panelSexo = document.getElementById('panel-sexo');
    const panelEdad = document.getElementById('panel-edad');
    const panelDescripcion = document.getElementById('panel-descripcion');
    const panelClinica = document.getElementById('panel-clinica');
    const panelContacto = document.getElementById('panel-contacto');

    const selectRegion = document.getElementById('id_region');
    const selectCiudad = document.getElementById('id_ciudad');

    let currentSelectedCard = null; // Para mantener el rastro de la tarjeta seleccionada

    // Función para abrir el panel
    function abrirPanel(mascotaData, clickedCard) {
        console.log('--- Inicia abrirPanel ---');
        console.log('mascotaData recibido en abrirPanel:', mascotaData);
        // Remover la clase 'selected' de la tarjeta previamente seleccionada
        if (currentSelectedCard && currentSelectedCard !== clickedCard) {
            currentSelectedCard.classList.remove('selected');
        }

        // Añadir la clase 'selected' a la tarjeta actual
        clickedCard.classList.add('selected');
        currentSelectedCard = clickedCard;

        // Rellenar el contenido del panel
        panelImagen.src = mascotaData.imagen;
        panelImagen.alt = mascotaData.nombre;
        panelNombre.textContent = mascotaData.nombre;
        panelEspecie.textContent = mascotaData.especie;
        panelRaza.textContent = mascotaData.raza;
        panelSexo.textContent = mascotaData.sexo;
        panelEdad.textContent = mascotaData.edad;
        panelDescripcion.textContent = mascotaData.descripcion;
        panelClinica.textContent = mascotaData.clinica;


        let edadTexto = mascotaData.edad;
        if (mascotaData.unidad_edad === 'meses') {
            edadTexto += ' meses';
        } else {
            edadTexto += ' años';
        }
        panelEdad.textContent = edadTexto;

        
        // ** ESTO ES LO CRÍTICO **
        console.log('mascotaData.id justo antes de construir URL:', mascotaData.id);
        if (mascotaData.id) {
            if (usuarioEstaLogueado === true) {
                panelContacto.href = `/adopciones/solicitar/${mascotaData.id}/`;
            } else {
                panelContacto.href = `${urlLogin}?next=/adopciones/solicitar/${mascotaData.id}/`;
            }
            console.log('URL de contacto establecida a:', panelContacto.href);
        } else {
            console.error("ERROR: mascotaData.id es undefined o nulo. Enlace de adopción no válido.");
            panelContacto.href = "#";
        }

        panelDetalles.classList.add('active');
        panelDetalles.scrollTop = 0;
        console.log('--- Fin abrirPanel ---');
    }

    // Función para cerrar el panel
    function cerrarPanel() {
        panelDetalles.classList.remove('active');
        // Remover la clase 'selected' de la tarjeta actual si existe
        if (currentSelectedCard) {
            currentSelectedCard.classList.remove('selected');
            currentSelectedCard = null;
        }
    }

    // Event Listeners para cada tarjeta de mascota
    tarjetasMascota.forEach(tarjeta => {
        tarjeta.addEventListener('click', function() {
            // Si la tarjeta clicada ya está seleccionada y el panel está activo, ciérralo
            if (this === currentSelectedCard && panelDetalles.classList.contains('active')) {
                cerrarPanel();
            } else {
                // Recopila los datos del data-attributes
                const mascota = {
                    id: tarjeta.dataset.id, // Capturamos el ID
                    nombre: tarjeta.dataset.nombre,
                    especie: tarjeta.dataset.especie,
                    edad: tarjeta.dataset.edad,
                    unidad_edad: tarjeta.dataset.unidadEdad, 
                    descripcion: tarjeta.dataset.descripcion,
                    imagen: tarjeta.dataset.imagen,
                    clinica: tarjeta.dataset.clinica,
                    sexo: tarjeta.dataset.sexo,
                    raza: tarjeta.dataset.raza
                };
                abrirPanel(mascota, this); // Pasamos la tarjeta clicada
            }
        });
    });
    // Event Listener para el botón de cerrar del panel
    cerrarPanelBtn.addEventListener('click', cerrarPanel);

    // Opcional: Cerrar el panel con la tecla Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && panelDetalles.classList.contains('active')) {
            cerrarPanel();
        }
    });

    // Opcional: Cerrar el panel si se hace clic en cualquier otro lugar fuera de las tarjetas o el panel
    document.addEventListener('click', function(event) {
        // Asegúrate de que el clic no sea en una tarjeta ni dentro del panel
        const isClickInsidePanel = panelDetalles.contains(event.target);
        const isClickOnCard = event.target.closest('.tarjeta-mascota');
        const isPanelActive = panelDetalles.classList.contains('active');

        if (isPanelActive && !isClickInsidePanel && !isClickOnCard) {
            cerrarPanel();
        }
    });
    if (!selectRegion || !selectCiudad) return;

        selectRegion.addEventListener('change', () => {
            const regionId = selectRegion.value;

            if (!regionId) {
            selectCiudad.innerHTML = '<option value="">Todas las ciudades</option>';
            selectCiudad.disabled = true;
            return;
            }

            fetch(`/ubicacion/api/ciudades/?region_id=${regionId}`)
            .then(response => response.json())
            .then(data => {
                selectCiudad.innerHTML = '<option value="">Todas las ciudades</option>';
                data.forEach(ciudad => {
                const option = document.createElement('option');
                option.value = ciudad.id;
                option.textContent = ciudad.nombre;
                selectCiudad.appendChild(option);
                });
                selectCiudad.disabled = false;
            })
            .catch(() => {
                selectCiudad.innerHTML = '<option value="">Error al cargar ciudades</option>';
                selectCiudad.disabled = true;
            });
        });

        // Desactivar selectCiudad si no hay selección
        if (!selectCiudad.options.length || selectCiudad.options.length <= 1) {
            selectCiudad.disabled = true;
        }





    


});