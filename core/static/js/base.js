document.addEventListener('DOMContentLoaded', function () {
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
    });