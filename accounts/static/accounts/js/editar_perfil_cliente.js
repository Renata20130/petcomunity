document.addEventListener('DOMContentLoaded', () => {
    const inputFoto = document.getElementById('id_imagen');
    const preview = document.getElementById('preview-imagen');

    if (!inputFoto || !preview) return;

    inputFoto.addEventListener('change', () => {
      const file = inputFoto.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  });