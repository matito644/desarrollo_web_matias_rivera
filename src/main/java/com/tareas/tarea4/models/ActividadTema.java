package com.tareas.tarea4.models;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;

@Entity
@Table(name = "actividad_tema")
class ActividadTema {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Enumerated(EnumType.STRING)
    @Column(name = "tema", nullable = false)
    private TipoTema tema;

    @Column(name = "glosa_otro", length = 15)
    private String glosaOtro;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actividad_id", nullable = false)
    @JsonIgnore
    private Actividad actividad;

    // Constructores
    public ActividadTema() {}

    public ActividadTema(TipoTema tema, Actividad actividad) {
        this.tema = tema;
        this.actividad = actividad;
    }

    // Getters y Setters
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public TipoTema getTema() {
        return tema;
    }

    public void setTema(TipoTema tema) {
        this.tema = tema;
    }

    public String getGlosaOtro() {
        return glosaOtro;
    }

    public void setGlosaOtro(String glosaOtro) {
        this.glosaOtro = glosaOtro;
    }

    public Actividad getActividad() {
        return actividad;
    }

    public void setActividad(Actividad actividad) {
        this.actividad = actividad;
    }
}