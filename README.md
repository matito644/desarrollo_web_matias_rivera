# Tarea 3 - Actividades Recreativas

Este proyecto es una aplicación web desarrollada con Flask para gestionar y mostrar actividades recreativas.

## Principales cambios

- Sección de estadísticas con gráficos (dinámica)
- Agregar y visualizar comentarios en las actividades


## Consideraciones

- Para el gráfico de torta (actividades por tema), cuando una actividad tiene más de un tema entonces se cuenta para cada uno de sus temas.
- Para el gráfico de barras (actividades por mes y horario) se utiliza la hora de inicio de la actividad para clasificar a la misma dentro de un horario del día, pudiendo ser mañana (antes de las 12:00), tarde (antes de las 18:00) y noche (antes de las 00:00).

Mención honrosa a Highcharts GPT para el estilo de los gráficos.


### Dependencias
- Python
- MySQL
- Ver `requirements.txt`
