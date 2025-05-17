from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from database.db import get_latest_activities, get_some_activities, get_activity_detail, save_activity, get_regions_and_communes
import json
import re
import datetime
import filetype

app = Flask(__name__)

# Configuración básica
app.config.update(
    SECRET_KEY='mega-secret-key',
    UPLOAD_FOLDER='static/uploads',
    TEMPLATES_AUTO_RELOAD=True
)

@app.route('/')
def index():
    # Obtenemos las últimas 5 actividades desde la base de datos
    ultimas_actividades = get_latest_activities(limit=5)

    # Verificamos si hay un mensaje de éxito en la sesión
    success_message = session.pop('success_message', None)

    return render_template('index.html', activities=ultimas_actividades, success_message=success_message)

@app.route('/agregar-actividad', methods=['GET', 'POST'])
def agregar_actividad():
    # Si la petición es GET
    if request.method == 'GET':
        return render_template('agregar_actividad.html')

    # Si la petición es POST
    if request.method == 'POST':
        # Verificamos si el formulario ha sido confirmado
        if request.form.get('confirmed') != 'true':
            # Si no ha sido confirmado, mostramos el formulario de nuevo
            return render_template('agregar_actividad.html', form_data=request.form)

        # Validamos los datos recibidos
        errors = validate_activity_form(request.form, request.files)

        if errors:
            # Si hay errores, mostramos el formulario de nuevo con los errores
            return render_template('agregar_actividad.html', form_data=request.form, error_message=", ".join(errors))

        # Procesamos y guardamos la actividad
        success, message = save_activity(request.form, request.files)
        if success:
            # Si todo salió bien, guardamos mensaje de éxito en la sesión y vamos a la página principal
            session['success_message'] = "Actividad agregada exitosamente."
            return redirect(url_for('index'))
        else:
            # Si no, mostramos el formulario de nuevo con el mensaje de error
            return render_template('agregar_actividad.html', form_data=request.form, error_message=message)

@app.route('/listado-actividades')
def listado_actividades():
    # Validamos que el parámetro page sea un entero
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        # Si no es un entero válido, usamos la página 1
        page = 1

    per_page = 5

    # Obtenemos las actividades para la página actual y el total de actividades
    current_activities, total_count = get_some_activities(page=page, per_page=per_page)

    # Calculamos el número total de páginas
    total_pages = (total_count + per_page - 1) // per_page

    # Ajustamos la página si está fuera de rango
    if page > total_pages and total_pages > 0:
        return redirect(url_for('listado_actividades', page=total_pages))

    return render_template(
        'listado_actividades.html',
        activities=current_activities,
        page=page,
        total_pages=total_pages,
        has_prev=(page > 1),
        has_next=(page < total_pages)
    )

@app.route('/detalle-actividad/<activity_id>')
def detalle_actividad(activity_id):
    # Validamos que el ID sea un número
    try:
        activity_id = int(activity_id)
    except ValueError:
        # Si no es un número válido, redirigimos al listado
        return redirect(url_for('listado_actividades'))

    # Obtenemos los detalles de la actividad usando su ID de la base de datos
    activity = get_activity_detail(activity_id)

    # Si no se encuentra, también redirigimos al listado
    if activity is None:
        return redirect(url_for('listado_actividades'))

    return render_template('detalle_actividad.html', activity=activity)

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')


# Función para validar campos del formulario
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

# Ruta para proporcionar las regiones y comunas en formato JSON
@app.route('/api/regiones-comunas')
def get_regiones_comunas_json():
    regions_data = get_regions_and_communes()
    return jsonify(regions_data)


if __name__ == '__main__':
    app.run(debug=True)
