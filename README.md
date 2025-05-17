# Tarea 2 - Actividades Recreativas

Este proyecto es una aplicación web desarrollada con Flask para gestionar y mostrar actividades recreativas. Permite a los usuarios agregar nuevas actividades, visualizar listados paginados y ver detalles de cada actividad individual.

## Características

- Registro de nuevas actividades recreativas con formulario completo
- Visualización de últimas actividades en la página principal
- Listado paginado de todas las actividades
- Vista detallada de cada actividad con imágenes
- Sección de estadísticas con gráficos (estática)

---

## Consideraciones

### Problema al validar los templates

Al validar archivos de plantillas Jinja2 (`.html`) con validadores HTML estándar, aparecen múltiples errores aunque el código funcione correctamente en la aplicación. Esto ocurre porque los validadores HTML tradicionales no están diseñados para entender la sintaxis de plantillas.


### Obtención de actividades recientes

Al usar `order_by(Actividad.dia_hora_inicio.desc())`, la consulta ordena estas fechas de manera que las más recientes (fechas mayores) aparecen antes que las más antiguas (fechas menores).

### Dependencias
- Python
- MySQL
- Ver `requirements.txt`
