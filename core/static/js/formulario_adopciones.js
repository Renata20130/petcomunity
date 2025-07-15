document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Cargado. Inicializando acordeón..."); // Mensaje de depuración
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    if (accordionHeaders.length === 0) {
        console.warn("No se encontraron elementos con la clase 'accordion-header'. Revisa tu HTML y los selectores CSS/JS.");
        return;
    }

    let activeHeader = null;

    accordionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const targetContent = document.getElementById(targetId);

            if (!targetContent) {
                console.error(`ERROR JS: Contenido objetivo con ID '${targetId}' no encontrado para el encabezado:`, this);
                return;
            }

            console.log(`Clic en encabezado: ${this.textContent}. Apuntando a ID: ${targetId}`);

            // Cierra el panel anteriormente activo si existe y no es el actual
            if (activeHeader && activeHeader !== this) {
                const activeTargetId = activeHeader.dataset.target;
                const activeTargetContent = document.getElementById(activeTargetId);

                console.log(`Cerrando panel anterior: ${activeHeader.textContent}`);
                activeHeader.classList.remove('active');
                if (activeTargetContent) {
                    activeTargetContent.classList.remove('show');
                }
            }

            // Alterna la clase 'active' en el encabezado clicado
            this.classList.toggle('active');
            // Alterna la clase 'show' en el contenido
            targetContent.classList.toggle('show');

            // Actualiza el encabezado activo
            if (this.classList.contains('active')) {
                activeHeader = this;
                console.log(`Panel abierto: ${this.textContent}`);
            } else {
                activeHeader = null;
                console.log(`Panel cerrado: ${this.textContent}`);
            }
        });
    });

    // Opcional: Descomenta para abrir el primer panel al cargar la página
    // if (accordionHeaders.length > 0) {
    //     accordionHeaders[0].click();
    // }
});