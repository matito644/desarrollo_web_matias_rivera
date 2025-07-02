package com.tareas.tarea4.models;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ActividadRepository extends JpaRepository<Actividad, Integer> {

    /**
     * Encuentra actividades realizadas ordenadas por fecha de termino (mas recientes primero)
     * Solo incluye actividades que tienen fecha de termino definida y anterior a la fecha actual
     */
    @Query("SELECT a FROM Actividad a WHERE a.diaHoraTermino IS NOT NULL AND a.diaHoraTermino < :fechaActual ORDER BY a.diaHoraTermino DESC")
    List<Actividad> findActividadesRealizadas(@Param("fechaActual") LocalDateTime fechaActual);
}