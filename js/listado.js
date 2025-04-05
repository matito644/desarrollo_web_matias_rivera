const initListado = () => {
  const actividades = [
    {
      inicio: "2025-09-01 10:00",
      termino: "2025-09-01 12:00",
      comuna: "Rancagua",
      sector: "Rancagua Sur",
      tema: "Natación",
      organizador: "Romina Hernández",
      totalFotos: 3,
      fotos: ["img/oshawott.png", "img/oshawott.png", "img/oshawott.png"],
    },
    {
      inicio: "2025-08-15 09:30",
      termino: "2025-08-15 11:00",
      comuna: "Rancagua",
      sector: "Rancagua Centro",
      tema: "Clases de astucia",
      organizador: "Franz Widerstrom",
      totalFotos: 2,
      fotos: ["img/oshawott.png", "img/oshawott.png"],
    },
    {
      inicio: "2025-07-20 14:00",
      termino: "2025-07-20 16:30",
      comuna: "Rancagua",
      sector: "Rancagua Norte",
      tema: "Mímica",
      organizador: "Matías Rivera",
      totalFotos: 4,
      fotos: [
        "img/oshawott.png",
        "img/oshawott.png",
        "img/oshawott.png",
        "img/oshawott.png",
      ],
    },
    {
      inicio: "2025-06-10 08:00",
      termino: "2025-06-10 10:00",
      comuna: "Rancagua",
      sector: "Rancagua Sur",
      tema: "Batallar épicamente",
      organizador: "Brayan Tamayo",
      totalFotos: 1,
      fotos: ["img/oshawott.png"],
    },
    {
      inicio: "2025-05-05 17:00",
      termino: "2025-05-05 19:00",
      comuna: "Rancagua",
      sector: "Rancagua Centro",
      tema: "Clases de ternura",
      organizador: "Pamela Seguel",
      totalFotos: 2,
      fotos: ["img/oshawott.png", "img/oshawott.png"],
    },
  ];

  // Almacenamos los datos en el localStorage para poder acceder a ellos en el detalle
  localStorage.setItem("actividades", JSON.stringify(actividades));

  const tbody = document.getElementById("actividadesTableBody");

  actividades.forEach((act, index) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${act.inicio}</td>
      <td>${act.termino}</td>
      <td>${act.comuna}</td>
      <td>${act.sector}</td>
      <td>${act.tema}</td>
      <td>${act.organizador}</td>
      <td>${act.totalFotos}</td>
    `;
    // Se ocupa el índice como parámetro
    tr.addEventListener("click", () => {
      window.location.href = `detalle-actividad.html?index=${index}`;
    });
    tbody.appendChild(tr);
  });
};

document.addEventListener("DOMContentLoaded", initListado);
