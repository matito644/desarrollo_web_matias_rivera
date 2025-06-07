let actividadId = null;

document.addEventListener("DOMContentLoaded", function () {
  // Obtenemos el ID de la actividad desde la URL
  const path = window.location.pathname;
  const pathSegments = path.split("/");
  if (pathSegments) {
    actividadId = parseInt(pathSegments[pathSegments.length - 1]);
    cargarComentarios();
    configurarFormulario();
  }
});

function configurarFormulario() {
  const form = document.getElementById("comentarioForm");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    enviarComentario();
  });
}

// Validamos el formulario
function validarFormulario() {
  const nombre = document.getElementById("nombreComentario").value.trim();
  const texto = document.getElementById("textoComentario").value.trim();
  const errors = [];

  if (!nombre) {
    errors.push("El nombre es obligatorio");
  } else if (nombre.length < 3) {
    errors.push("El nombre debe tener al menos 3 caracteres");
  } else if (nombre.length > 80) {
    errors.push("El nombre no puede exceder 80 caracteres");
  }

  if (!texto) {
    errors.push("El texto del comentario es obligatorio");
  } else if (texto.length < 5) {
    errors.push("El comentario debe tener al menos 5 caracteres");
  } else if (texto.length > 300) {
    errors.push("El comentario no puede exceder 300 caracteres");
  }

  return {
    valid: errors.length === 0,
    errors: errors,
    data: { nombre, texto },
  };
}

// Enviamos el comentario al servidor
function enviarComentario() {
  const validation = validarFormulario();

  // Limpiamos mensajes anteriores
  ocultarMensajes();

  if (!validation.valid) {
    mostrarError(validation.errors.join(", "));
    return;
  }

  const datos = {
    actividad_id: actividadId,
    nombre: validation.data.nombre,
    texto: validation.data.texto,
  };

  // Hacemos el post con fetch
  fetch("/api/comentarios", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datos),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        mostrarExito(data.message);
        limpiarFormulario();
        cargarComentarios();
      } else {
        mostrarError(data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      mostrarError("Error al enviar el comentario. Inténtalo de nuevo.");
    });
}

// Cargamos comentarios desde el servidor
function cargarComentarios() {
  if (!actividadId) return;

  const container = document.getElementById("comentariosContainer");
  if (!container) return;

  container.innerHTML = '<div class="loading">Cargando comentarios...</div>';

  fetch(`/api/comentarios/${actividadId}`)
    .then((response) => response.json())
    .then((comentarios) => {
      mostrarComentarios(comentarios);
    })
    .catch((error) => {
      console.error("Error cargando comentarios:", error);
      container.innerHTML =
        '<div class="error">Error al cargar comentarios</div>';
    });
}

// Mostramos los comentarios
function mostrarComentarios(comentarios) {
  const container = document.getElementById("comentariosContainer");
  if (!container) return;

  if (comentarios.length === 0) {
    container.innerHTML =
      '<div class="no-comentarios">No hay comentarios aún. ¡Sé el primero!</div>';
    return;
  }

  let html = "";
  comentarios.forEach((comentario) => {
    html += `
            <div class="comentario-item">
                <div class="comentario-header">
                    <strong class="comentario-nombre">${escapeHtml(comentario.nombre)}</strong>
                    <span class="comentario-fecha">${comentario.fecha}</span>
                </div>
                <div class="comentario-texto">
                    ${escapeHtml(comentario.texto)}
                </div>
            </div>
        `;
  });

  container.innerHTML = html;
}

// Funciones útiles
function mostrarError(mensaje) {
  const errorDiv = document.getElementById("comentarioError");
  if (errorDiv) {
    errorDiv.textContent = mensaje;
    errorDiv.style.display = "block";
  }
}

function mostrarExito(mensaje) {
  const successDiv = document.getElementById("comentarioSuccess");
  if (successDiv) {
    successDiv.textContent = mensaje;
    successDiv.style.display = "block";
  }
}

function ocultarMensajes() {
  const errorDiv = document.getElementById("comentarioError");
  const successDiv = document.getElementById("comentarioSuccess");

  if (errorDiv) errorDiv.style.display = "none";
  if (successDiv) successDiv.style.display = "none";
}

function limpiarFormulario() {
  const form = document.getElementById("comentarioForm");
  if (form) {
    form.reset();
  }
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
