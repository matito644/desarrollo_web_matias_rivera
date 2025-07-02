package com.tareas.tarea4.models;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "actividad")
public class Actividad {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "dia_hora_inicio", nullable = false)
    private LocalDateTime diaHoraInicio;

    @Column(name = "dia_hora_termino")
    private LocalDateTime diaHoraTermino;

    @Column(name = "sector", length = 100)
    private String sector;

    @Column(name = "nombre", nullable = false, length = 200)
    private String nombre;

    @OneToMany(mappedBy = "actividad", fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    private List<ActividadTema> temas;

    @OneToMany(mappedBy = "actividad", fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    private List<Nota> notas;

    // Constructores
    public Actividad() {}

    public Actividad(String nombre, LocalDateTime diaHoraInicio) {
        this.nombre = nombre;
        this.diaHoraInicio = diaHoraInicio;
    }

    /**
     * Calcula el promedio de las notas de la actividad
     * @return Promedio de las notas o null si no hay notas
     */
    @JsonProperty("promedioNotas")
    public Double getPromedioNotas() {
        if (notas == null || notas.isEmpty()) {
            return null;
        }

        double suma = notas.stream()
                .mapToInt(Nota::getNota)
                .average()
                .orElse(0.0);

        return suma;
    }

    // Getters y Setters
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public LocalDateTime getDiaHoraInicio() {
        return diaHoraInicio;
    }

    public void setDiaHoraInicio(LocalDateTime diaHoraInicio) {
        this.diaHoraInicio = diaHoraInicio;
    }

    public LocalDateTime getDiaHoraTermino() {
        return diaHoraTermino;
    }

    public void setDiaHoraTermino(LocalDateTime diaHoraTermino) {
        this.diaHoraTermino = diaHoraTermino;
    }

    public String getSector() {
        return sector;
    }

    public void setSector(String sector) {
        this.sector = sector;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public List<ActividadTema> getTemas() {
        return temas;
    }

    public void setTemas(List<ActividadTema> temas) {
        this.temas = temas;
    }

    public List<Nota> getNotas() {
        return notas;
    }

    public void setNotas(List<Nota> notas) {
        this.notas = notas;
    }
}