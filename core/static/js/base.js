document.addEventListener('DOMContentLoaded', function () {
    // Toggle submenu perfil
    const btn = document.querySelector('.btn-perfil');
    const submenu = document.querySelector('.submenu');
    
    if (btn && submenu) {
        btn.addEventListener('click', function (e) {
            e.stopPropagation(); // Evita que el clic cierre el menú inmediatamente
            // Alterna visibilidad con display block/none
            if (submenu.style.display === 'block') {
                submenu.style.display = 'none';
            } else {
                submenu.style.display = 'block';
            }
        });

        // Cierra submenu al hacer clic fuera
        document.addEventListener('click', function () {
            submenu.style.display = 'none';
        });
    }

    // Toggle menú hamburguesa
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }
});
