document.addEventListener('DOMContentLoaded', function () {
      // Toggle submenu perfil
      const btn = document.querySelector('.btn-perfil');
      const submenu = document.querySelector('.submenu');

      if (btn && submenu) {
        btn.addEventListener('click', function (e) {
          e.stopPropagation();
          submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
        });

        document.addEventListener('click', function () {
          submenu.style.display = 'none';
        });
      }

        const menuToggle = document.getElementById('menu-toggle');
        const navLinks = document.getElementById('nav-links');
        const navIcons = document.querySelector('.nav-icons-actions');

        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            navIcons.classList.toggle('active');
        });

    
});