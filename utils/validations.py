import re
import datetime
import filetype

def validate_activity_form(form_data, files):
    errors = []

    # Validamos campos obligatorios
    required_fields = {
        'comuna_id': 'Comuna',
        'nombre': 'Nombre del organizador',
        'email': 'Email',
        'dia_hora_inicio': 'Día y hora de inicio'
    }

    for field, field_name in required_fields.items():
        if not form_data.get(field):
            errors.append(f"El campo {field_name} es obligatorio")

    # Validamos el email
    if form_data.get('email'):
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, form_data.get('email')):
            errors.append("El formato del email no es válido")

    # Validamos el teléfono
    if form_data.get('celular'):
        phone_regex = r'^\+\d{3}\.\d{8}$'
        if not re.match(phone_regex, form_data.get('celular')):
            errors.append("El formato del número de celular debe ser +NNN.NNNNNNNN")

    # Validamos que haya al menos una foto
    if 'foto' not in files:
        errors.append("Debe incluir al menos una foto")
    else:
        foto_files = files.getlist('foto')
        valid_photos = [f for f in foto_files if f and f.filename]

        if len(valid_photos) < 1:
            errors.append("Debe incluir al menos una foto")
        elif len(valid_photos) > 5:
            errors.append("Solo se permiten hasta 5 fotos")

        # Validamos los tipos de archivos
        for foto in valid_photos:
            try:
                tipo = filetype.guess(foto)
                if not tipo or tipo.mime.split('/')[0] != 'image':
                    errors.append(f"El archivo {foto.filename} no es una imagen válida")
            except Exception:
                errors.append(f"Error al verificar el tipo de archivo {foto.filename}")

    # Validamos que se haya seleccionado al menos un tema
    temas_seleccionados = [key for key in form_data.keys() if key.startswith('tema-')]
    if not temas_seleccionados:
        errors.append("Debe seleccionar al menos un tema")

    # Validamos el tema "otro"
    if 'tema-otro' in form_data:
        if not form_data.get('glosa_otro'):
            errors.append("Debe incluir la descripción del tema otro")
        elif len(form_data.get('glosa_otro')) < 3 or len(form_data.get('glosa_otro')) > 15:
            errors.append("La descripción del tema otro debe tener entre 3 y 15 caracteres")

    # Validamos las fechas
    try:
        if form_data.get('dia_hora_inicio'):
            inicio = datetime.datetime.fromisoformat(form_data.get('dia_hora_inicio'))

            if form_data.get('dia_hora_termino'):
                termino = datetime.datetime.fromisoformat(form_data.get('dia_hora_termino'))
                if termino <= inicio:
                    errors.append("La fecha de término debe ser posterior a la fecha de inicio")
    except ValueError:
        errors.append("El formato de fecha no es válido")

    # Validamos las opciones de contacto
    contact_options = ['whatsapp', 'telegram', 'instagram', 'tiktok', 'x', 'otra']
    checked_options = [opt for opt in contact_options if opt in form_data]

    for option in checked_options:
        option_id = f"{option}-id"
        if option_id in form_data:
            if len(form_data.get(option_id)) < 4 or len(form_data.get(option_id)) > 50:
                errors.append(f"El ID de {option} debe tener entre 4 y 50 caracteres")
        else:
            errors.append(f"Falta el ID para la opción de contacto {option}")

    return errors

# Validamos que el comentario que se intenta agregar sea válido
def validate_comment(actividad_id, nombre, texto):
    errors = []

    if not actividad_id:
        errors.append('ID de actividad es requerido')

    if not nombre:
        errors.append('El nombre es obligatorio')
    elif len(nombre) < 3:
        errors.append('El nombre debe tener al menos 3 caracteres')
    elif len(nombre) > 80:
        errors.append('El nombre no puede exceder 80 caracteres')

    if not texto:
        errors.append('El texto del comentario es obligatorio')
    elif len(texto) < 5:
        errors.append('El comentario debe tener al menos 5 caracteres')
    elif len(texto) > 300:
        errors.append('El comentario no puede exceder 300 caracteres')

    return errors
