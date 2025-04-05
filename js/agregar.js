// Elementos del formulario
const activityForm = document.getElementById("activityForm");

// Sección ¿Dónde?
const regionSelect = document.getElementById("regionSelect");
const comunaSelect = document.getElementById("comunaSelect");
const sectorValue = document.getElementById("sectorInput").value;

// Sección ¿Quién organiza?
const organizerName = document.getElementById("organizerName");
const organizerEmail = document.getElementById("organizerEmail");
const organizerPhone = document.getElementById("organizerPhone");
const contactCheckboxes = document.querySelectorAll(
  "#contactGroup input[type='checkbox']",
);

// Sección ¿Cuándo y de qué trata?
const startTime = document.getElementById("startTime");
const endTime = document.getElementById("endTime");
const descripcion = document.getElementById("descripcion");
const tema = document.getElementById("tema");
const otroTemaContainer = document.getElementById("otroTemaContainer");
const otroTema = document.getElementById("otroTema");
const fotoContainer = document.getElementById("fotoContainer");
const addPhotoButton = document.getElementById("addPhotoButton");

// Botones del modal de confirmación y mensaje final
const confirmationModal = document.getElementById("confirmationModal");
const confirmYes = document.getElementById("confirmYes");
const confirmNo = document.getElementById("confirmNo");
const finalMessage = document.getElementById("finalMessage");
const backToHome = document.getElementById("backToHome");

let regionesData = [];

// Función para formatear número con cero a la izquierda
function pad(num) {
  return num.toString().padStart(2, "0");
}

// Función para sumar 3 horas a una fecha
function sum3Hours(date) {
  return new Date(date.getTime() + 3 * 60 * 60 * 1000);
}

// Prellenar el campo de inicio y término
function setDefaultDateTimes() {
  const now = new Date();
  const formattedNow =
    now.getFullYear() +
    "-" +
    pad(now.getMonth() + 1) +
    "-" +
    pad(now.getDate()) +
    "T" +
    pad(now.getHours()) +
    ":" +
    pad(now.getMinutes());
  startTime.value = formattedNow;

  const later = sum3Hours(now);
  const formattedLater =
    later.getFullYear() +
    "-" +
    pad(later.getMonth() + 1) +
    "-" +
    pad(later.getDate()) +
    "T" +
    pad(later.getHours()) +
    ":" +
    pad(later.getMinutes());
  endTime.value = formattedLater;
}

// Actualiza el campo de término al cambiar la hora de inicio
startTime.addEventListener("change", () => {
  const startDate = new Date(startTime.value);
  const newEndDate = sum3Hours(startDate);
  const formattedNewEnd =
    newEndDate.getFullYear() +
    "-" +
    pad(newEndDate.getMonth() + 1) +
    "-" +
    pad(newEndDate.getDate()) +
    "T" +
    pad(newEndDate.getHours()) +
    ":" +
    pad(newEndDate.getMinutes());
  endTime.value = formattedNewEnd;
});

// Controlamos que solo se seleccionen hasta 5 opciones en "Contactar por"
function toggleContactInput(element) {
  if (element.checked) {
    let checkedBoxes = document.querySelectorAll(
      "#contactGroup input[type='checkbox']:checked",
    );
    if (checkedBoxes.length > 5) {
      alert("Solo se pueden seleccionar hasta 5 opciones de contacto.");
      element.checked = false;
      return;
    }
  }
  const inputElem = document.getElementById("contact-" + element.name);
  if (element.checked) {
    inputElem.style.display = "inline-block";
  } else {
    inputElem.style.display = "none";
    inputElem.value = "";
  }
}

// Mostrar u ocultar el input para tema "otro"
tema.addEventListener("change", () => {
  if (tema.value === "otro") {
    otroTemaContainer.style.display = "block";
  } else {
    otroTemaContainer.style.display = "none";
    otroTema.value = "";
  }
});

// Funciones para cargar regiones y comunas
function loadRegiones() {
  fetch("region_comuna.json")
    .then((response) => response.json())
    .then((data) => {
      regionesData = data.regiones;
      populateRegiones();
    });
}
function populateRegiones() {
  regionesData.forEach((region) => {
    const option = document.createElement("option");
    option.value = region.id;
    option.textContent = region.nombre;
    regionSelect.appendChild(option);
  });
}
function updateComunas() {
  const regionId = regionSelect.value;
  comunaSelect.innerHTML = '<option value="">-- Seleccione Comuna --</option>';
  if (regionId) {
    const region = regionesData.find((r) => r.id == regionId);
    if (region && region.comunas) {
      region.comunas.forEach((comuna) => {
        const option = document.createElement("option");
        option.value = comuna.id;
        option.textContent = comuna.nombre;
        comunaSelect.appendChild(option);
      });
    }
  }
}

// Agregar otra foto
addPhotoButton.addEventListener("click", () => {
  // Contar cuántos inputs file hay en fotoContainer
  const currentFiles =
    fotoContainer.querySelectorAll("input[type='file']").length;
  if (currentFiles >= 5) {
    alert("Solo se permiten hasta 5 fotos.");
    return;
  }
  const newInput = document.createElement("input");
  newInput.type = "file";
  newInput.name = "foto";
  newInput.accept = "image/*";
  fotoContainer.appendChild(newInput);
});

// Validadores básicos
const validateSelect = (value) => value !== "";
const validateText = (text, minLength = 0, maxLength = Infinity) =>
  text.trim().length >= minLength && text.trim().length <= maxLength;

// Función de validación general del formulario
const validateForm = (e) => {
  // Con esto no quitamos los valores que ya ingresó el usuario al intentar validar el formulario
  e.preventDefault();
  let invalidInputs = [];
  let isValid = true;

  // Sección ¿Dónde?
  if (!validateSelect(regionSelect.value)) {
    invalidInputs.push("Región");
    isValid = false;
  }
  if (!validateSelect(comunaSelect.value)) {
    invalidInputs.push("Comuna");
    isValid = false;
  }
  if (!validateText(sectorValue, 0, 100)) {
    invalidInputs.push("Sector (máx. 100 caracteres)");
    isValid = false;
  }

  // Sección ¿Quién organiza?
  if (!validateText(organizerName.value, 1, 200)) {
    invalidInputs.push("Nombre (requerido, máx. 200 caracteres)");
    isValid = false;
  }
  if (!validateText(organizerEmail.value, 1, 100)) {
    invalidInputs.push("Email (requerido, máx. 100 caracteres)");
    isValid = false;
  } else {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(organizerEmail.value)) {
      invalidInputs.push("Email (formato inválido)");
      isValid = false;
    }
  }
  if (organizerPhone.value.trim() !== "") {
    const phoneRegex = /^\+\d{3}\.\d{8}$/;
    if (!phoneRegex.test(organizerPhone.value.trim())) {
      invalidInputs.push("Número de celular (formato +NNN.NNNNNNNN)");
      isValid = false;
    }
  }
  contactCheckboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      const inputElement = document.getElementById("contact-" + checkbox.name);
      let detail = inputElement.value.trim();
      if (!validateText(detail, 4, 50)) {
        invalidInputs.push(
          "Contacto " + checkbox.name + " (4 a 50 caracteres)",
        );
        isValid = false;
      }
    }
  });

  // Sección ¿Cuándo y de qué trata?
  if (!startTime.value) {
    invalidInputs.push("Día hora inicio");
    isValid = false;
  }
  if (endTime.value) {
    const startDate = new Date(startTime.value);
    const endDate = new Date(endTime.value);
    if (endDate <= startDate) {
      invalidInputs.push("Día hora término debe ser mayor que inicio");
      isValid = false;
    }
  }
  if (tema.value === "") {
    invalidInputs.push("Tema");
    isValid = false;
  }
  if (tema.value === "otro") {
    if (!validateText(otroTema.value, 3, 15)) {
      invalidInputs.push("Descripción del tema (3 a 15 caracteres)");
      isValid = false;
    }
  }
  // Validar que haya entre 1 y 5 fotos
  const files = fotoContainer.querySelectorAll("input[type='file']");
  let totalFiles = 0;
  files.forEach((input) => {
    if (input.files && input.files.length > 0) {
      totalFiles += input.files.length;
    }
  });
  if (totalFiles < 1) {
    invalidInputs.push("Debe seleccionarse al menos 1 foto");
    isValid = false;
  } else if (totalFiles > 5) {
    invalidInputs.push("Solo se permiten hasta 5 fotos");
    isValid = false;
  }

  if (!isValid) {
    alert(
      "Por favor, corrija los siguientes campos:\n- " +
        invalidInputs.join("\n- "),
    );
    return;
  }

  // Si la validación es correcta, mostramos el modal de confirmación
  confirmationModal.classList.add("active");
};

// Dependiendo de la respuesta podemos ocultar un modal y mostrar otro
confirmYes.addEventListener("click", () => {
  confirmationModal.classList.remove("active");
  finalMessage.classList.add("active");
});
confirmNo.addEventListener("click", () => {
  confirmationModal.classList.remove("active");
});
backToHome.addEventListener("click", () => {
  window.location.href = "index.html";
});

document.addEventListener("DOMContentLoaded", () => {
  loadRegiones();
  regionSelect.addEventListener("change", updateComunas);
  setDefaultDateTimes();
  activityForm.addEventListener("submit", validateForm);
});
