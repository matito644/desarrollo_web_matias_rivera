from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from werkzeug.utils import secure_filename
import datetime
import os
import hashlib
import filetype
import uuid

# Configuramos la conexión con la DB
DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelos de la base de datos
class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    comunas = relationship('Comuna', backref='region', lazy=True)

class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    actividades = relationship('Actividad', backref='comuna', lazy=True)

class Actividad(Base):
    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime, nullable=True)
    descripcion = Column(String(500), nullable=True)
    fotos = relationship('Foto', backref='actividad', lazy=True)
    contactos = relationship('ContactarPor', backref='actividad', lazy=True)
    temas = relationship('ActividadTema', backref='actividad', lazy=True)

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

class ActividadTema(Base):
    __tablename__ = 'actividad_tema'
    id = Column(Integer, primary_key=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
    glosa_otro = Column(String(15), nullable=True)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

# Esta función obtiene las últimas actividades desde la base de datos
def get_latest_activities(limit=5):
    try:
        session = SessionLocal()
        # Consultamos las últimas actividades
        actividades_db = session.query(Actividad).order_by(Actividad.dia_hora_inicio.desc()).limit(limit).all()

        result = []
        for act in actividades_db:
            fotos = session.query(Foto).filter_by(actividad_id=act.id).all()
            foto_url = fotos[0].ruta_archivo if fotos else ""

            # Obtenemos todos los temas de la actividad
            temas = session.query(ActividadTema).filter_by(actividad_id=act.id).all()
            temas_list = [tema.tema for tema in temas]
            temas_str = ", ".join(temas_list)

            result.append({
                "inicio": act.dia_hora_inicio.strftime("%Y-%m-%d %H:%M"),
                "termino": act.dia_hora_termino.strftime("%Y-%m-%d %H:%M") if act.dia_hora_termino else "-",
                "comuna": act.comuna.nombre,
                "sector": act.sector if act.sector else "",
                "tema": temas_str,
                "foto": foto_url
            })

        return result
    except Exception as e:
        print(f"Error al obtener actividades: {str(e)}")
        return []
    finally:
        session.close()

# Esta función obtiene actividades paginadas desde la base de datos
def get_some_activities(page=1, per_page=5):
    try:
        session = SessionLocal()

        # Calculamos offset para la paginación
        offset = (page - 1) * per_page

        # Consultamos el número total de actividades
        total_count = session.query(Actividad).count()

        # Obtenemos solo las actividades para la página actual
        actividades_db = session.query(Actividad)\
            .offset(offset)\
            .limit(per_page)\
            .all()

        activities = []
        for act in actividades_db:
            fotos = session.query(Foto).filter_by(actividad_id=act.id).all()

            # Obtenemos todos los temas de la actividad
            temas = session.query(ActividadTema).filter_by(actividad_id=act.id).all()
            temas_list = [tema.tema for tema in temas]
            temas_str = ", ".join(temas_list)

            activities.append({
                "inicio": act.dia_hora_inicio.strftime("%Y-%m-%d %H:%M"),
                "termino": act.dia_hora_termino.strftime("%Y-%m-%d %H:%M") if act.dia_hora_termino else "",
                "comuna": act.comuna.nombre,
                "sector": act.sector if act.sector else "",
                "tema": temas_str,
                "organizador": act.nombre,
                "totalFotos": len(fotos),
                "id": act.id
            })

        return activities, total_count
    except Exception as e:
        print(f"Error al obtener actividades paginadas: {str(e)}")
        return [], 0
    finally:
        session.close()

# Esta función obtiene los detalles de una actividad específica
def get_activity_detail(id):
    try:
        session = SessionLocal()
        # Buscamos la actividad en la base de datos
        act_db = session.query(Actividad).get(id)

        if act_db:
            fotos = session.query(Foto).filter_by(actividad_id=id).all()
            fotos_urls = [foto.ruta_archivo for foto in fotos]

            # Obtenemos todos los temas de la actividad
            temas = session.query(ActividadTema).filter_by(actividad_id=id).all()
            temas_list = [tema.tema for tema in temas]
            temas_str = ", ".join(temas_list)

            return {
                "inicio": act_db.dia_hora_inicio.strftime("%Y-%m-%d %H:%M"),
                "termino": act_db.dia_hora_termino.strftime("%Y-%m-%d %H:%M") if act_db.dia_hora_termino else "",
                "comuna": act_db.comuna.nombre,
                "sector": act_db.sector if act_db.sector else "",
                "tema": temas_str,
                "organizador": act_db.nombre,
                "totalFotos": len(fotos),
                "fotos": fotos_urls
            }
        return None
    except Exception as e:
        print(f"Error al obtener detalle de actividad: {str(e)}")
        return None
    finally:
        session.close()

# Esta función se encarga de guardar una nueva actividad en la base de datos
# Asume que los datos ya fueron validados
def save_activity(form_data, files):
    session = SessionLocal()
    try:
        # Obtenemos datos del formulario
        comuna_id = form_data.get('comuna_id')
        sector = form_data.get('sector', '')
        nombre = form_data.get('nombre')
        email = form_data.get('email')
        celular = form_data.get('celular', '')
        dia_hora_inicio = form_data.get('dia_hora_inicio')
        dia_hora_termino = form_data.get('dia_hora_termino', '')
        descripcion = form_data.get('descripcion', '')

        # Convertimos las fechas a objetos datetime
        inicio_dt = datetime.datetime.fromisoformat(dia_hora_inicio)
        termino_dt = datetime.datetime.fromisoformat(dia_hora_termino) if dia_hora_termino else None

        # Creamos una nueva actividad
        nueva_actividad = Actividad(
            comuna_id=comuna_id,
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            dia_hora_inicio=inicio_dt,
            dia_hora_termino=termino_dt,
            descripcion=descripcion
        )

        # Guardamos en la base de datos
        session.add(nueva_actividad)
        session.flush()  # Para obtener el ID de la actividad

        # Procesamos los temas
        tema_prefijo = 'tema-'
        temas_keys = [key for key in form_data.keys() if key.startswith(tema_prefijo)]

        for tema_key in temas_keys:
            tema_valor = tema_key[len(tema_prefijo):]  # Extraemos el valor después del prefijo

            # Mapeamos los valores del formulario a los valores del enum
            tema_mapping = {
                'musica': 'música',
                'deporte': 'deporte',
                'ciencias': 'ciencias',
                'religion': 'religión',
                'politica': 'política',
                'tecnologia': 'tecnología',
                'juegos': 'juegos',
                'baile': 'baile',
                'comida': 'comida',
                'otro': 'otro'
            }

            tema_enum_valor = tema_mapping.get(tema_valor, tema_valor)

            glosa_otro = form_data.get('glosa_otro', '') if tema_valor == 'otro' else None

            nuevo_tema = ActividadTema(
                tema=tema_enum_valor,
                glosa_otro=glosa_otro,
                actividad_id=nueva_actividad.id
            )
            session.add(nuevo_tema)

        # Procesamos las opciones de contacto
        for opcion in ['whatsapp', 'telegram', 'instagram', 'tiktok', 'x', 'otra']:
            if opcion in form_data and f'{opcion}-id' in form_data:
                contacto = ContactarPor(
                    nombre=opcion,
                    identificador=form_data.get(f'{opcion}-id'),
                    actividad_id=nueva_actividad.id
                )
                session.add(contacto)

        # Procesamos las fotos
        fotos_files = files.getlist('foto')
        for foto in fotos_files:
            if foto and foto.filename:
                filename_hash = hashlib.sha256(
                    secure_filename(foto.filename).encode("utf-8")
                    ).hexdigest()

                extension = filetype.guess(foto).extension

                img_filename = f"{filename_hash}_{str(uuid.uuid4())}.{extension}"

                # Crear la carpeta de uploads si no existe
                uploads_dir = os.path.join('static', 'uploads')
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)

                # Guardamos la foto
                foto_path = os.path.join(uploads_dir, img_filename)
                foto.save(foto_path)

                # Registramos la foto en la base de datos
                nueva_foto = Foto(
                    ruta_archivo=f"/static/uploads/{img_filename}",
                    nombre_archivo=img_filename,
                    actividad_id=nueva_actividad.id
                )
                session.add(nueva_foto)

        # Guardamos todos los cambios
        session.commit()
        return True, "Actividad agregada exitosamente."

    except Exception as e:
        # Revertimos cambios en caso de error
        session.rollback()
        return False, f"Error al agregar la actividad: {str(e)}"
    finally:
        session.close()

# Esta función obtiene todas las regiones y sus comunas para formato JSON
def get_regions_and_communes():
    try:
        session = SessionLocal()
        regions = session.query(Region).order_by(Region.nombre).all()

        result = {"regiones": []}
        for region in regions:
            communes = session.query(Comuna).filter_by(region_id=region.id).order_by(Comuna.nombre).all()

            communes_list = [{"id": comuna.id, "nombre": comuna.nombre} for comuna in communes]

            result["regiones"].append({
                "id": region.id,
                "nombre": region.nombre,
                "comunas": communes_list
            })

        return result
    except Exception as e:
        print(f"Error al obtener regiones y comunas: {str(e)}")
        return {"regiones": []}
    finally:
        session.close()
