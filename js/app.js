// Datos de ejemplo para las últimas 5 actividades
const activities = [
  {
    inicio: "2025-04-01 10:00",
    termino: "2025-04-01 12:00",
    comuna: "Santiago",
    sector: "Centro",
    tema: "Duelo",
    foto: "img/oshawott-mini.jpeg",
  },
  {
    inicio: "2025-04-02 09:30",
    termino: "2025-04-02 11:30",
    comuna: "Providencia",
    sector: "Norte",
    tema: "Toma de la Bastilla",
    foto: "img/oshawott-mini.jpeg",
  },
  {
    inicio: "2025-04-03 14:00",
    termino: "2025-04-03 16:00",
    comuna: "Las Condes",
    sector: "Oeste",
    tema: "Caminata grupal",
    foto: "img/oshawott-mini.jpeg",
  },
  {
    inicio: "2025-04-04 08:00",
    termino: "2025-04-04 10:00",
    comuna: "Maipú",
    sector: "Sur",
    tema: "Carrera pokemon",
    foto: "img/oshawott-mini.jpeg",
  },
  {
    inicio: "2025-04-05 18:00",
    termino: "",
    comuna: "San Miguel",
    sector: "Este",
    tema: "Evento Cultural",
    foto: "img/oshawott-mini.jpeg",
  },
];

// Insertamos los datos en la tabla
const tableBody = document.getElementById("activitiesTableBody");
activities.forEach((activity) => {
  const row = document.createElement("tr");

  // Celda para la fecha de inicio
  const inicioCell = document.createElement("td");
  inicioCell.textContent = activity.inicio;
  row.appendChild(inicioCell);

  // Celda para la fecha de término
  const terminoCell = document.createElement("td");
  terminoCell.textContent = activity.termino || "-";
  row.appendChild(terminoCell);

  // Celda para la comuna
  const comunaCell = document.createElement("td");
  comunaCell.textContent = activity.comuna;
  row.appendChild(comunaCell);

  // Celda para el sector
  const sectorCell = document.createElement("td");
  sectorCell.textContent = activity.sector;
  row.appendChild(sectorCell);

  // Celda para el tema
  const temaCell = document.createElement("td");
  temaCell.textContent = activity.tema;
  row.appendChild(temaCell);

  // Celda para la foto
  const fotoCell = document.createElement("td");
  const img = document.createElement("img");
  img.src = activity.foto;
  img.alt = activity.tema;
  img.style.width = "80px";
  fotoCell.appendChild(img);
  row.appendChild(fotoCell);

  tableBody.appendChild(row);
});
