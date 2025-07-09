// accounts/static/accounts/js/profile_menu.js

document.addEventListener('DOMContentLoaded', function() {
    const profileToggle = document.querySelector('.profile-toggle');
    const profileDropdown = document.querySelector('.profile-dropdown');

    if (profileToggle && profileDropdown) {
        profileToggle.addEventListener('click', function() {
            profileDropdown.classList.toggle('show');
            profileToggle.classList.toggle('active'); // Añade/elimina la clase 'active' para la rotación de la flecha
        });

        // Cierra el desplegable si el usuario hace clic fuera de él
        window.addEventListener('click', function(event) {
            if (!profileToggle.contains(event.target) && !profileDropdown.contains(event.target)) {
                profileDropdown.classList.remove('show');
                profileToggle.classList.remove('active');
            }
        });
    }
});