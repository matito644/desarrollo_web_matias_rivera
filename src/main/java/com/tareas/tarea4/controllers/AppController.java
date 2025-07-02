package com.tareas.tarea4.controllers;

import com.tareas.tarea4.models.Actividad;
import com.tareas.tarea4.services.ApiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class AppController {

    @Autowired
    private ApiService apiService;

    /**
     * Landing page que muestra las actividades realizadas
     */
    @GetMapping("/")
    public String index(Model model) {
        try {
            List<Actividad> actividadesRealizadas = apiService.getActividadesRealizadas();
            model.addAttribute("activities", actividadesRealizadas);
        } catch (Exception e) {
            // En caso de error, mandamos una lista vacia
            model.addAttribute("activities", List.of());
        }

        return "index";
    }
}