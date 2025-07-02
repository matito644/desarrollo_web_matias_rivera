package com.tareas.tarea4.services;

import com.tareas.tarea4.models.Actividad;
import com.tareas.tarea4.models.ActividadRepository;
import com.tareas.tarea4.models.Nota;
import com.tareas.tarea4.models.NotaRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class ApiService {

    @Autowired
    private ActividadRepository actividadRepository;

    @Autowired
    private NotaRepository notaRepository;

    /**
     * Obtiene todas las actividades realizadas ordenadas por fecha de termino (mas recientes primero)
     * @return Lista de actividades realizadas ordenadas
     */
    public List<Actividad> getActividadesRealizadas() {
        LocalDateTime ahora = LocalDateTime.now();
        return actividadRepository.findActividadesRealizadas(ahora);
    }

    /**
     * Agrega una nueva nota a una actividad
     * @param actividadId ID de la actividad
     * @param valorNota Valor de la nota (1-7)
     * @return Map con el resultado de la operacion
     */
    @Transactional
    public Map<String, Object> agregarNota(Integer actividadId, Integer valorNota) {
        Map<String, Object> respuesta = new HashMap<>();

        try {
            // Verificamos que la actividad existe
            Optional<Actividad> actividadOpt = actividadRepository.findById(actividadId);
            if (actividadOpt.isEmpty()) {
                respuesta.put("error", "Actividad no encontrada");
                return respuesta;
            }

            Actividad actividad = actividadOpt.get();

            // Creamos y guardamos la nueva nota
            Nota nuevaNota = new Nota(actividad, valorNota);
            notaRepository.save(nuevaNota);

            // Recalculamos el promedio
            actividad = actividadRepository.findById(actividadId).get();
            Double nuevoPromedio = actividad.getPromedioNotas();

            respuesta.put("success", true);
            respuesta.put("mensaje", "Nota agregada exitosamente");
            respuesta.put("actividadId", actividadId);
            respuesta.put("nuevaNota", valorNota);
            respuesta.put("nuevoPromedio", nuevoPromedio);
            respuesta.put("totalNotas", actividad.getNotas().size());

            return respuesta;

        } catch (Exception e) {
            respuesta.put("error", "Error al agregar la nota");
            respuesta.put("detalle", e.getMessage());
            return respuesta;
        }
    }
}