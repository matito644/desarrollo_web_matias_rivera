package com.tareas.tarea4.controllers;

import com.tareas.tarea4.models.Actividad;
import com.tareas.tarea4.services.ApiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class ApiController {

    @Autowired
    private ApiService apiService;

    /**
     * GET /api/actividades-realizadas
     * Obtiene todas las actividades que han terminado ordenadas por fecha de termino (mas recientes primero)
     */
    @GetMapping("/actividades-realizadas")
    public ResponseEntity<List<Actividad>> getActividadesRealizadas() {
        try {
            List<Actividad> actividades = apiService.getActividadesRealizadas();
            return ResponseEntity.ok(actividades);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    /**
     * POST /api/actividades/{id}/notas
     * Agrega una nueva nota a una actividad
     */
    @PostMapping("/actividades/{actividadId}/notas")
    public ResponseEntity<Map<String, Object>> agregarNota(
            @PathVariable Integer actividadId,
            @RequestBody Map<String, Integer> request) {
        try {
            Integer valorNota = request.get("nota");

            // Validamos que la nota esta entre 1 y 7
            if (valorNota == null || valorNota < 1 || valorNota > 7) {
                Map<String, Object> error = new HashMap<>();
                error.put("error", "La nota debe ser un número entero entre 1 y 7");
                return ResponseEntity.badRequest().body(error);
            }

            // Agregamos la nota usando el servicio
            Map<String, Object> resultado = apiService.agregarNota(actividadId, valorNota);

            if (resultado.containsKey("error")) {
                return ResponseEntity.badRequest().body(resultado);
            }

            return ResponseEntity.ok(resultado);

        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Error interno del servidor");
            error.put("mensaje", e.getMessage());
            return ResponseEntity.internalServerError().body(error);
        }
    }
}