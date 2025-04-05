# Actividades Recreativas

Este proyecto es una aplicación web para la gestión de actividades recreativas. La aplicación permite agregar nuevas actividades, listar las últimas actividades, ver detalles de cada actividad y consultar estadísticas (no reales) a través de gráficos. A continuación se describen las principales decisiones tomadas en el desarrollo, así como detalles importantes que se deben tener en cuenta.

## Estructura del Proyecto

El repositorio se organiza de la siguiente forma:

- **t1/**
  - **css/**
    - style.css → Define los estilos generales y específicos para la interfaz, incluyendo animaciones y transiciones para indicar al usuario las áreas interactivas.
  - **js/**
    - app.js → Se encarga de cargar y mostrar las últimas 5 actividades en la portada.
    - agregar.js → Maneja la lógica para el formulario de agregar actividades, validaciones y actualización de campos.
    - listado.js → Muestra el listado completo de actividades, que permiten navegar al detalle correspondiente.
    - detalle.js → Controla la visualización del detalle de una actividad, con funcionalidad para ampliar imágenes al hacer clic en ellas.
  - **Archivos HTML:**
    - index.html → Portada donde se presentan las últimas actividades y un menú de navegación simple.
    - agregar-actividad.html → Página para agregar una nueva actividad.
    - listado-actividades.html → Listado completo de actividades.
    - detalle-actividad.html → Pantalla de detalle de una actividad.
    - estadisticas.html → Muestra gráficos de las actividades.


## Principales Decisiones y Funcionalidades

- **Imagen repetida para las actividades:**
  En este proyecto se utiliza una imagen de muestra (por ejemplo, "img/oshawott-mini.jpeg" o "img/oshawott.png") para todas las actividades.
  Esto se hizo para simplificar la carga visual en las diferentes secciones (listado, detalles, portada) y se puede cambiar en el futuro para que cada actividad tenga imágenes únicas.

- **Actualización automática de la hora de término:**
  Se implementó una función en el archivo `agregar.js` que actualiza automáticamente el campo de la hora de término de la actividad.
  Cada vez que el usuario modifique el campo de hora de inicio, la hora de término se ajusta sumándole 3 horas.
  Esto garantiza que la hora de término sea consistente y evita errores de configuración en el formulario.

- **Animaciones y efectos interactivos con CSS:**
  La hoja de estilos `style.css` incluye algunas animaciones y transiciones que mejoran la experiencia de usuario:
  - Se aplica un efecto hover en las filas del listado de actividades, indicándole al usuario que son campos clicables para ver el detalle de la actividad.
  - Los botones y otros elementos interactivos cuentan con transiciones de color para mejorar la usabilidad y visualización de interacciones.

- **Validaciones en el formulario:**
  El formulario para agregar actividades cuenta con validaciones de campos obligatorios y formatos específicos (por ejemplo, formato de email, teléfono y validaciones para los campos de contacto).
  Se limita la cantidad de elementos (fotos, opciones de contacto) permitidos.

- **Gestión de regiones y comunas:**
  Se implementa el uso de un archivo JSON (mediante `fetch`) para la carga de regiones y comunas.
