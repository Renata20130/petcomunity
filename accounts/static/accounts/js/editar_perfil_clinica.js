document.getElementById('id_imagen').addEventListener('change', function(event) {
        const preview = document.getElementById('preview-imagen');
        const file = event.target.files[0];
        if (file) {
            preview.src = URL.createObjectURL(file);
        }
    });

    // Script para agregar días en horarios (mantener y ajustar para que el nuevo formset clone de un elemento existente)
    document.getElementById('agregar-dia').addEventListener('click', function () {
        const container = document.getElementById('formset-container');
        const totalForms = document.getElementById('id_form-TOTAL_FORMS');
        let formCount = parseInt(totalForms.value);

        // Clona la última fila existente o crea una nueva si no hay (asegúrate de que siempre haya un elemento para clonar en el template, aunque sea vacío)
        let lastForm = document.querySelector('.horario-item-compact.formset-form:last-child');
        let newForm;

        if (lastForm) {
            newForm = lastForm.cloneNode(true);
        } else {
            // Fallback si no hay ningún formulario en el formset (debería haber al menos 1 por Django)
            newForm = document.createElement('div');
            newForm.classList.add('horario-item-compact', 'formset-form');
            // Aquí deberías rellenar con la estructura HTML de un horario vacío si es posible,
            // o asegurarte que Django siempre rinda al menos un formulario vacío con `extra=1` en tu formset.
            newForm.innerHTML = `
                <div class="campo-horario-compact"><select name="form-${formCount}-dia" id="id_form-${formCount}-dia">
                    <option value="1">Lunes</option><option value="2">Martes</option>... </select></div>
                <div class="campo-horario-compact"><input type="time" name="form-${formCount}-hora_inicio" id="id_form-${formCount}-hora_inicio"></div>
                <div class="campo-horario-compact"><input type="time" name="form-${formCount}-hora_fin" id="id_form-${formCount}-hora_fin"></div>
                <div class="campo-horario-compact delete-checkbox-compact">
                    <input type="checkbox" name="form-${formCount}-DELETE" id="id_form-${formCount}-DELETE"> <label for="id_form-${formCount}-DELETE"></label>
                    <input type="hidden" name="form-${formCount}-id" id="id_form-${formCount}-id">
                </div>
            `;
        }

        newForm.querySelectorAll('input, select, label').forEach(node => {
            if (node.id) {
                node.id = node.id.replace(/form-(\d+)/, `form-${formCount}`);
            }
            if (node.name) {
                node.name = node.name.replace(/form-(\d+)/, `form-${formCount}`);
            }
            if (node.htmlFor) {
                node.htmlFor = node.htmlFor.replace(/form-(\d+)/, `form-${formCount}`);
            }

            if (node.type === 'checkbox' || node.type === 'radio') {
                node.checked = false;
            } else if (node.tagName === 'INPUT' || node.tagName === 'SELECT') {
                node.value = '';
            }
        });

        const idInput = newForm.querySelector('input[id$="-id"]');
        if (idInput) {
            idInput.value = '';
        }

        container.appendChild(newForm);
        totalForms.value = formCount + 1;
    });

    // --- Script para la navegación del sidebar ---
    document.addEventListener('DOMContentLoaded', function() {
        const navItems = document.querySelectorAll('.nav-item');
        const contentSections = document.querySelectorAll('.content-section');
        const formElement = document.querySelector('.perfil-form'); // Asume que todo está dentro de este formulario

        function showSection(sectionId) {
            contentSections.forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(sectionId).classList.add('active');

            navItems.forEach(item => {
                item.classList.remove('active');
            });
            document.querySelector(`.nav-item[data-section="${sectionId}"]`).classList.add('active');
        }

        navItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const targetSection = this.getAttribute('data-section');
                showSection(targetSection);
            });
        });

        // Manejar el envío del formulario para que incluya todos los datos
        // Cuando se envía el formulario, todos los campos ocultos deben ser incluidos.
        // Django maneja esto automáticamente si los campos están dentro del mismo <form> tag.
        // El único ajuste que podríamos necesitar es si el formset no está visible al momento de enviar,
        // pero Django envía todos los campos con sus `name` y `id` correctos.
        // Asegúrate de que tu vista de Django maneje los datos de ambas secciones.
        formElement.addEventListener('submit', function(event) {
            // Opcional: Podrías hacer alguna validación JS antes de enviar,
            // o simplemente permitir que Django maneje la validación del formulario completo.
            console.log("Formulario enviado. Todos los campos visibles o no, serán enviados.");
        });

        // Mostrar la primera sección por defecto al cargar la página
        // showSection('info-personal'); // Ya lo está haciendo el HTML si tiene 'active' en el primero
    });
    regionSelect.addEventListener('change', function () {
        const regionSelect = document.getElementById('id_region');
        const ciudadSelect = document.getElementById('id_ciudad');

        if (regionSelect && ciudadSelect) {
            regionSelect.addEventListener('change', function () {
                const regionId = this.value;

            ciudadSelect.innerHTML = '<option value="">---------</option>';

            if (!regionId) return;

            fetch(`/ubicacion/ajax/cargar-ciudades/?region_id=${regionId}`)
                .then(response => response.json())
                .then(data => {
                    data.ciudades.forEach(ciudad => {
                        const option = document.createElement('option');
                        option.value = ciudad.id;
                        option.textContent = ciudad.nombre;
                        ciudadSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error("Error al cargar ciudades:", error);
                });
        });
    }
});