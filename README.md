# Tarea 4 - Actividades Recreativas

Este proyecto es una aplicación web desarrollada con Spring Boot para evaluar actividades recreativas.

## Consideraciones

Me tomé bastante en serio lo de que solo hay que implementar lo que se pide en la tarea:

- Implementé directamente en `index.html` todo.
- Solo conservé los estilos (CSS) necesarios.
- Solo implementé los modelos necesarios, es decir, los que quiero se muestren en la página, incluyendo los campos de *Nota*.
- Se ocupan alertas para pedir la nota al usuario y para mostrar mensajes, por lo mismo es necesario interactuar con las alertas para que recién ahí se actualice el nuevo promedio en la tabla, no es lo óptimo pero funciona.
- Hago las llamadas asíncronas con `fetch`.
- Si bien la gran mayoría de getters y setters no se ocupa, los quise mantener.
- Investigué un poco y el uso de `@Transactional` es óptimo en `ApiService` porque estoy haciendo múltiples llamados a la base de datos, así todo se ejecuta como una unidad atómica.
