const initDetalle = () => {
  const obtenerParametro = (nombre) => {
    const params = new URLSearchParams(window.location.search);
    return params.get(nombre);
  };

  const actividades = JSON.parse(localStorage.getItem("actividades"));
  const index = obtenerParametro("index");

  const act = actividades[index];
  const contenedor = document.getElementById("detalleActividad");

  // Creamos la tabla con el contenido
  let html = `
    <table class="detalle-table">
      <tr><th>Inicio</th><td>${act.inicio}</td></tr>
      <tr><th>Término</th><td>${act.termino}</td></tr>
      <tr><th>Comuna</th><td>${act.comuna}</td></tr>
      <tr><th>Sector</th><td>${act.sector}</td></tr>
      <tr><th>Tema</th><td>${act.tema}</td></tr>
      <tr><th>Organizador</th><td>${act.organizador}</td></tr>
      <tr><th>Total Fotos</th><td>${act.totalFotos}</td></tr>
    </table>
    <h2>Fotos de la Actividad</h2>
    <div class="fotos-container">
  `;

  // Incluimos las imágenes en el HTML
  act.fotos.forEach((fotoURL, idx) => {
    html += `<img src="${fotoURL}" alt="Foto ${idx + 1}" class="miniPhoto" width="320" height="240" />`;
  });
  html += `</div>`;
  contenedor.innerHTML = html;

  // Ampliar las imágenes cuando se les hace clic
  const miniPhotos = document.querySelectorAll(".miniPhoto");
  const modal = document.getElementById("photoModal");
  const imgContainer = document.getElementById("imgContainer");
  const closeModal = document.getElementById("closeModal");

  miniPhotos.forEach((img) => {
    img.addEventListener("click", () => {
      const modalImg = document.createElement("img");
      modalImg.src = img.src.replace("320x240", "800x600");
      modalImg.alt = "Foto ampliada";
      imgContainer.innerHTML = "";
      imgContainer.appendChild(modalImg);
      modal.classList.add("active");
    });
  });

  // Cerramos la imagen cuando se presiona la X o se pierde el foco
  closeModal.addEventListener("click", () => modal.classList.remove("active"));
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove("active");
    }
  });
};

document.addEventListener("DOMContentLoaded", initDetalle);
