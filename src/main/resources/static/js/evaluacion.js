function evaluarActividad(actividadId) {
    // Solicitamos la nota al usuario
    const nota = prompt("Ingrese una nota para esta actividad (1-7):");

    if (nota === null) {
        return;
    }

    const valorNota = parseInt(nota);

    // Validamos que sea un entero entre 1 y 7
    if (isNaN(valorNota) || valorNota < 1 || valorNota > 7) {
        alert("Error: La nota debe ser un número entero entre 1 y 7");
        return;
    }

    // Deshabilitamos el boton mientras se procesa
    const boton = document.getElementById(`btn-evaluar-${actividadId}`);
    const textoOriginal = boton.textContent;
    boton.disabled = true;
    boton.textContent = "Guardando...";

    // Realizamos la llamada asincrona con fetch
    fetch(`/api/actividades/${actividadId}/notas`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nota: valorNota })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizamos el promedio en la interfaz
                const elementoPromedio = document.getElementById(`promedio-${actividadId}`);
                if (data.nuevoPromedio !== null) {
                    elementoPromedio.textContent = data.nuevoPromedio.toFixed(1);
                } else {
                    elementoPromedio.textContent = '-';
                }

                // Mostramos el mensaje de exito
                alert(`Nota ${valorNota} agregada exitosamente.`);
            } else {
                // Mostramos un error
                alert(`Error: ${data.error || 'No se pudo agregar la nota'}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión. Favor perdonar.');
        })
        .finally(() => {
            // Rehabilitamos el boton
            boton.disabled = false;
            boton.textContent = textoOriginal;
        });
}