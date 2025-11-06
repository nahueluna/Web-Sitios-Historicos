import datetime
import os
from uuid import uuid1
from flask import current_app
from os import abort, fstat
from src.web.decorator import block_admin_maintenance
from src.core.models.auth import get_usuario_by_email
from src.core.models.auth.user import RolUsuario
from src.core.models.images import guardar_imagenes
from src.web.handlers.auth import login_required, role_required
from src.core.models.historic_site_tags import get_tags_by_site
from src.core.models.search import get_all_tags
from flask import Blueprint, render_template, request, jsonify, session
from src.core.models.historic_sites import delete_histoirc_site, get_historic_site, list_all_historic_sites, list_visible_historic_sites, add_historic_site, edit_historic_site
from core.models.historic_sites import list_historic_sites_with_filters
from src.core.models.historic_sites_categorie import delete_category, list_historic_sites_categorie, add_category
from src.core.models.historic_sites_state import list_states
from src.core.models.historic_sites_logs import get_logs_per_hs
import io, csv
from datetime import datetime
from flask import Response

from src.web.decorator import block_admin_maintenance


historic_sites_bp = Blueprint('historic_sites', __name__, url_prefix='/sitios-historicos')

# -- USUARIOS -- #

# RENDERING
@historic_sites_bp.route('/explore') # Renderiza html
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def render_index(_user):
    tags = get_all_tags()
    return render_template('/historic_sites/index.html', tags=tags)

@historic_sites_bp.route('/detalle/<int:id>') # Renderiza html
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def render_detail(user, id):
    return render_template('historic_sites/historic_site_detail.html')
# RENDERING

@historic_sites_bp.route('/get-all', methods=['GET']) # Retorna todos los sitios historicos de la BD
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def get_all(user):
    json = [x.json() for x in list_all_historic_sites()]
    return jsonify(json), 200


# Endpoint para generar CSV del lado del servidor
@historic_sites_bp.route('/admin/export-sites', methods=['GET'])
@role_required([RolUsuario.ADMIN])
def export_sites(user):
    # Obtener parámetros de la query string
    params = request.args.to_dict()
    
    # Pasar page como None para que no aplique valor por default/reemplazar actual
    params['page'] = None  
    params['per_page'] = None
    
    try:
        tags = params.pop('tags')
        if tags:
            tags = tags.split(',')
            params['tags'] = tags
        (sites, total) = list_historic_sites_with_filters(**params)
        data = [x.json() for x in sites]
    except Exception as e:
        print(f"Error obteniendo sitios: {e}")
        return jsonify({
            "error": "Error aplicando filtros"
        }), 500

    # Devolver si no hay sitios
    if len(data) == 0:
        return jsonify({
            "error": "No hay datos para exportar"
        }), 404

    # Obtengo id y nombre correspondiente a cada categoria y estado
    categories = {cat.id: cat.category for cat in list_historic_sites_categorie()}
    states = {state.id: state.state for state in list_states()}

    # Diccionario para definir las columnas en español y poder manejar en el for los valores correspondientes
    # Excluyo la descripcion larga, fusiono las coordenadas y excluyo cualquier otro dato nuevo que no este definido aca
    column_translation = {
        "id": "ID del sitio",
        "site_name": "Nombre",
        "short_description": "Descripcion breve",
        "city": "Ciudad",
        "province": "Provincia",
        "status": "Estado de conservacion",
        "registration_date": "Fecha de registro",
        "inauguration_year": "Año de inauguracion",
        "category": "Categoria",
        "visible": "Visible"
    }

    fieldnames = list(column_translation.values()) + ["Coordenadas de geolocalizacion"] + ["Tags asociados"]

    # StringIO sirve para crear un archivo en memoria, en este caso CSV
    output = io.StringIO()

    # Agregar BOM para UTF-8. Marca invisible para que Excel reconozca UTF-8, por mas que ya se defina en el mimetype
    output.write('\ufeff')

    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=",")
    writer.writeheader()

    for row in data:
        # Creo una nueva fila
        spanish_row = {}

        # Obtener los tags del sitio en cada iteracion
        site_tags = get_tags_by_site(row['id'])  # Lista de objetos Tag
        tag_names = [tag.name for tag in site_tags]  # Extraer solo los nombres
        spanish_row["Tags asociados"] = " ; ".join(tag_names) if tag_names else "Sin tags"

        # Clave (ingles) valor (español) en el diccionario.
        for english_col, spanish_col in column_translation.items():
            # Si existe una columna con ese nombre en ingles en donde estoy parado
            if english_col in row:
                # Agarro el status_id o category_id y en base al diccionario lo reemplazo por el nombre correspondiente
                # El metodo get busca la clave del 1er param en el diccionario para entonces agarrar el valor, y si no la encuentra devuelve el segundo parametro (fallback)
                if english_col == "status":
                    spanish_row[spanish_col] = states.get(row[english_col], row[english_col])
                elif english_col == "category":
                    spanish_row[spanish_col] = categories.get(row[english_col], row[english_col])
                else:
                    spanish_row[spanish_col] = row[english_col]

        # Combino latitud y longitud (si existen) en una sola columna
        if 'latitude' in row and 'longitude' in row:
            spanish_row["Coordenadas de geolocalizacion"] = f"{row['latitude']}; {row['longitude']}"

        # Escribir fila transformada
        writer.writerow(spanish_row)

    # Nombre como lo solicita el documento
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f"sitios_{timestamp}.csv"

    # Response recibe el contenido en formato de string (getvalue), el mimetype o tipo de archivo (csv con codificacion utf-8)
    response = Response(output.getvalue(), mimetype="text/csv; charset=utf-8")
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response, 200


@historic_sites_bp.route('/get-site/<int:id>', methods=['GET']) # Retorna un sitio historico específico por ID
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def get_site(user, id):
    hs = get_historic_site(int(id))
    response = {
        "historic_site": hs[0].json(),
        "category": hs[1].category,
        "state": hs[2].state,
    }
    return jsonify(response), 200

# -- USUAIROS -- #

# -- ADMIN -- #

# RENDERING
@historic_sites_bp.route('/admin/gestion-sitios')  # Renderiza html
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
@block_admin_maintenance
def render_admin_management(_user):
    return render_template('/historic_sites/gestion_sitios.html')

@historic_sites_bp.route('/admin/')  # Renderiza html
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
@block_admin_maintenance
def render_admin_sites(_user):
    tags = get_all_tags()
    return render_template('/historic_sites/index.html', tags=tags)

@historic_sites_bp.route('/admin/agregar-sitio') # 
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def render_site_form(user):
    return render_template('historic_sites/add_historic_site.html')

@historic_sites_bp.route('/admin/editar-sitio/<int:id>') # 
@block_admin_maintenance
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def render_edite_site_form(user, id):
    return render_template('historic_sites/edit_historic_site.html')

@historic_sites_bp.route('/admin/categorias') # 
@block_admin_maintenance
@role_required([RolUsuario.ADMIN])
def render_admin_categories(user):
    return render_template('historic_sites/category/categories.html')

@historic_sites_bp.route('/admin/categorias/agregar') # 
@block_admin_maintenance
@role_required([RolUsuario.ADMIN])
def render_category_form(user):
    return render_template('historic_sites/category/add_category.html')

# RENDERING

@historic_sites_bp.route('/add-site', methods=['POST'])
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
@block_admin_maintenance
def add_site(user):
    try:
        form = request.form
        __validator__(form)
        files = request.files.getlist("images")

        if len(files) == 0:
            return jsonify({"error": "El sitio debe tener imagenes."}), 400

        client = current_app.storage

        # Guardar imagenes en Minio
        object_names = []
        titles = []
        descs = []
        bucket_name = current_app.config["MINIO_BUCKET"]
        for i, f in enumerate(files):
            _, ext = os.path.splitext(f.filename)
            ext = ext.lower()
            size = fstat(f.fileno()).st_size
            object_name = f"public/{str(uuid1())}{ext}"
            object_names.append(object_name)
            print(f"size: {size}")
            client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=f,
                length=size,
                content_type=f.content_type,
            )
            title = form.get(f"title_{i}")
            if len(title) > 100:
                return jsonify({"error": "Los titulos no pueden tener mas de 100 caracteres."}), 400
            titles.append(title)

            desc = form.get(f"description_{i}")
            if len(desc) > 300:
                return jsonify({"error": "Las descripciones no pueden tener mas de 300 caracteres."}), 400
            descs.append(desc)

        date_str = form.get("inauguration_year")
        inauguration_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        user_id = user.id

        hs = add_historic_site(
            site_name=form.get("site_name"),
            short_description=form.get("short_description"),
            long_description=form.get("long_description"),
            city=form.get("city"),
            province=form.get("province"),
            latitude=float(form.get("latitude")),
            longitude=float(form.get("longitude")),
            inauguration_year=inauguration_date,
            visible=(form.get("visible") == "True"),
            conservation_status=form.get("conservation_status"),
            category=form.get("category"),
            tags=form.getlist("tags"),
            user_id=user_id
        )

        guardar_imagenes(object_names, titles, descs, hs.id)

        return jsonify({}), 201

    except Exception as e:
        print("Error in add_site:", e)
        return jsonify({"error": str(e)}), 400

@historic_sites_bp.route('/edit-site', methods=['PUT'])
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
@block_admin_maintenance
def edit_site(user):
    try:
        json = request.get_json()
        __validator__(json)
        user_id = user.id

        date = json['inauguration_year']
        format_date = datetime.strptime(date, "%Y-%m-%d")
        format_date = format_date.strftime("%Y-%m-%d")

        edit_historic_site(
            hs_id = int(json['id']),
            site_name=json['site_name'],
            short_description=json['short_description'],
            long_description=json['long_description'],
            city=json['city'],
            province=json['province'],
            latitude=float(json['latitude']),
            longitude=float(json['longitude']),
            inauguration_year=format_date,
            visible=json['visible'],
            conservation_status=json['conservation_status'],       
            category=json['category'],
            tags=json.get('tags'),
            user_id=user_id
        )

        return jsonify({}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@historic_sites_bp.route('/delete-site', methods=['DELETE'])
@block_admin_maintenance
@role_required([RolUsuario.ADMIN])
def delete_site(user):
    try:
        id = request.get_json()['id']
        delete_histoirc_site(hs_id=int(id), user_id=user.id)

        return jsonify({}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -- ADMIN -- #

# -- AUXILIARES -- #
@historic_sites_bp.route('/category/get-all', methods=['GET']) # Retorna todas las categorias de sitios historicos de la BD
@role_required([RolUsuario.ADMIN])
def get_all_cateorie(user):
    json = [x.json() for x in list_historic_sites_categorie()]
    return jsonify(json), 200

@historic_sites_bp.route('/category/add-category', methods=['POST'])
@role_required([RolUsuario.ADMIN])
def admin_add_category(user):
    try:
        json = request.get_json()
        add_category(category_name=json["category"])
        return jsonify({}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@historic_sites_bp.route('/category/delete', methods=['DELETE'])
@role_required([RolUsuario.ADMIN])
def admin_delete_category(user):
    try:
        id = request.get_json()["id"]
        delete_category(c_id=id)
        return jsonify({}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@historic_sites_bp.route('/state/get-all', methods=['GET']) # Retorna todas los estados de sitios historicos de la BD
def get_all_states():
    return jsonify([x.json() for x in list_states()]), 200

@historic_sites_bp.route('/logs/get-all/<int:id>', methods=['GET']) # Retorna todas los estados de sitios historicos de la BD
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def get_all_logs(user, id):
    list =get_logs_per_hs(hs_id=id)
    response = []

    for log, email in list: 
        response.append(
            {
                "log_date": log.log_date,
                "user_email": email,
                "action_type": log.action_type
            }
        )
    
    return jsonify(response), 200

@historic_sites_bp.route('/tags/get-all', methods = ['GET'])
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def __get_all_tags(user):
    tags = get_all_tags()

    return jsonify([x.json() for x in tags]), 200

@historic_sites_bp.route('/tags/site-tags/<int:id>', methods = ['GET'])
def __get_all_tags_by_site(id):
    list = get_tags_by_site(id)
    return jsonify([x.json() for x in list]), 200

def __validator__(json: dict):
    # Validaciones individuales
    if not json.get('site_name'):  # Esto cubre None y cadena vacía
        raise ValueError("El nombre del sitio histórico no puede estar vacío")

    if not json.get('short_description'):
        raise ValueError("La descripción corta no puede estar vacía")

    if not json.get('long_description'):
        raise ValueError("La descripción larga no puede estar vacía")

    if not json.get('city'):
        raise ValueError("La ciudad no puede estar vacía")

    if not json.get('province'):
        raise ValueError("La provincia no puede estar vacía")

    if not json.get('inauguration_year'):
        raise ValueError("El año de inauguración no puede estar vacío")

    # Validación para coordenadas numéricas
    try:
        latitude = float(json['latitude'])
    except (TypeError, ValueError, KeyError):
        raise ValueError("La latitud debe ser un número válido")

    try:
        longitude = float(json['longitude'])
    except (TypeError, ValueError, KeyError):
        raise ValueError("La longitud debe ser un número válido")

# -- AUXILIARES -- #

