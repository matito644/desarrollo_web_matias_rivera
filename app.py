from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from database.db import (
    get_latest_activities,
    get_some_activities,
    get_activity_detail,
    save_activity,
    get_regions_and_communes,
    get_activities_by_day,
    get_activities_by_theme,
    get_activities_by_month_and_time,
    get_comments_by_activity,
    save_comment
)
from utils.validations import validate_activity_form, validate_comment
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

# APIs para obtener datos de estadísticas
@app.route('/api/estadisticas/por-dia')
def api_actividades_por_dia():
    data = get_activities_by_day()
    return jsonify(data)

@app.route('/api/estadisticas/por-tema')
def api_actividades_por_tema():
    data = get_activities_by_theme()
    return jsonify(data)

@app.route('/api/estadisticas/por-mes-horario')
def api_actividades_por_mes_horario():
    data = get_activities_by_month_and_time()
    return jsonify(data)

# Ruta para proporcionar las regiones y comunas en formato JSON
@app.route('/api/regiones-comunas')
def get_regiones_comunas_json():
    regions_data = get_regions_and_communes()
    return jsonify(regions_data)

# Ruta para obtener los comentarios asociados a una actividad
@app.route('/api/comentarios/<actividad_id>')
def get_comentarios(actividad_id):
    # Validamos que el ID sea un número
    try:
        actividad_id = int(actividad_id)
    except ValueError:
        # Si no es un número válido, retornamos una lista vacía
        return []
    comentarios = get_comments_by_activity(actividad_id)
    return jsonify(comentarios)

@app.route('/api/comentarios', methods=['POST'])
def agregar_comentario():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400

    actividad_id = data.get('actividad_id')
    nombre = data.get('nombre', '').strip()
    texto = data.get('texto', '').strip()

    # Validamos los datos
    errors = validate_comment(actividad_id, nombre, texto)

    if errors:
        return jsonify({'success': False, 'message': ', '.join(errors)}), 400

    # Guardamos el comentario
    success, message = save_comment(actividad_id, nombre, texto)

    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message}), 500

if __name__ == '__main__':
    app.run(debug=True)
