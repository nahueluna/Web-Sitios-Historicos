from os import abort
from src.core.models.auth import get_usuario_by_email
from src.core.models.auth.user import RolUsuario
from src.web.handlers.auth import login_required, role_required
from src.core.models.historic_site_tags import get_tags_by_site
from src.core.models.search import get_all_tags
from flask import Blueprint, render_template, request, jsonify, session
from src.core.models.historic_sites import delete_histoirc_site, get_historic_site, list_all_historic_sites, list_visible_historic_sites, add_historic_site, edit_historic_site
from src.core.models.historic_sites_categorie import list_historic_sites_categorie, add_category
from src.core.models.historic_sites_state import list_states
from src.core.models.historic_sites_logs import get_logs_per_hs
import pickle

historic_sites_bp = Blueprint('historic_sites', __name__, url_prefix='/sitios-historicos')

# -- USUAIROS -- #

# RENDERING
@historic_sites_bp.route('/') # Renderiza html
@login_required
def render_index(): return render_template('/historic_sites/index.html')

@historic_sites_bp.route('/detalle/<int:id>') # Renderiza html
@login_required
def render_detail(id): 
    user_email = session.get("user")
    user = get_usuario_by_email(user_email)
    is_admin = user.rol == RolUsuario.ADMIN
    has_access = user.rol in [RolUsuario.ADMIN, RolUsuario.EDITOR]
    return render_template('historic_sites/historic_site_detail.html', is_admin=is_admin, has_access=has_access)
# RENDERING

@historic_sites_bp.route('/get-all', methods=['GET']) # Retorna todos los sitios historicos de la BD
def get_all(): 
    # PREGUNTAR SESION PARA MOSTRATR TODOS O SOLO VISIBLES
    json = [x.json() for x in list_all_historic_sites()]
    return jsonify(json), 201

@historic_sites_bp.route('/get-site/<int:id>', methods=['GET']) # Retorna un sitio historico específico por ID
def get_site(id):
    hs = get_historic_site(int(id))

    response = {
        "historic_site": hs[0].json(),
        "category": hs[1].category,
        "state": hs[2].state,
    }
    return jsonify(response), 201

# -- USUAIROS -- #

# -- ADMIN -- #

# RENDERING
@historic_sites_bp.route('/admin/gestion-sitios')  # Renderiza html
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def render_admin_management(user): 
    # PREGUNTAR SI TIENE PERMISIOS
    is_admin = user.rol == RolUsuario.ADMIN
    return render_template('/historic_sites/gestion_sitios.html', is_admin=is_admin)

@historic_sites_bp.route('/admin/')  # Renderiza html
@login_required
def render_admin_sites(): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('/historic_sites/index.html')

@historic_sites_bp.route('/admin/agregar-sitio') # 
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def render_site_form(user): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('historic_sites/add_historic_site.html')

@historic_sites_bp.route('/admin/editar-sitio/<int:id>') # 
@role_required([RolUsuario.ADMIN, RolUsuario.EDITOR])
def render_edite_site_form(user, id): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('historic_sites/edit_historic_site.html')

@historic_sites_bp.route('/admin/categorias') # 
@role_required([RolUsuario.ADMIN])
def render_admin_categories(user): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('historic_sites/category/categories.html')

@historic_sites_bp.route('/admin/categorias/agregar') # 
@role_required([RolUsuario.ADMIN])
def render_category_form(user): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('historic_sites/category/add_category.html')

# RENDERING

@historic_sites_bp.route('/add-site', methods=['POST']) # 
def add_site(): 
    try:
        json = request.get_json()
        __validator__(json)
        user_email = session.get("user")
        user_id = get_usuario_by_email(user_email).id
        hs = add_historic_site(
            site_name=json['site_name'],
            short_description=json['short_description'],
            long_description=json['long_description'],
            city=json['city'],
            province=json['province'],
            latitude=json['latitude'],
            longitude=json['longitude'],
            inauguration_year=json['inauguration_year'],  
            visible=json['visible'],
            conservation_status=json['conservation_status'],       
            category=json['category'],
            tags=json.get('tags'),
            user_id=user_id
        )

        return jsonify({}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": e.args}), 400

@historic_sites_bp.route('/edit-site', methods=['PUT'])
def edit_site(): 
    try:
        json = request.get_json()
        __validator__(json)
        user_email = session.get("user")
        user_id = get_usuario_by_email(user_email).id
        edit_historic_site(
            hs_id = int(json['id']),
            site_name=json['site_name'],
            short_description=json['short_description'],
            long_description=json['long_description'],
            city=json['city'],
            province=json['province'],
            latitude=float(json['latitude']),
            longitude=float(json['longitude']),
            inauguration_year=json['inauguration_year'],  
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
def delete_site(): 
    try:
        id = request.get_json()['id']
        delete_histoirc_site(hs_id=int(id))

        return jsonify({}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -- ADMIN -- #

# -- AUXILIARES -- #
@historic_sites_bp.route('/category/get-all', methods=['GET']) # Retorna todas las categorias de sitios historicos de la BD
def get_all_cateorie():
    return jsonify([x.json() for x in list_historic_sites_categorie()]), 201 

@historic_sites_bp.route('/category/add-category', methods=['POST'])
def admin_add_category(): 
    json = request.get_json()
    add_category(category_name=json["category"])
    return jsonify({}), 201

@historic_sites_bp.route('/state/get-all', methods=['GET']) # Retorna todas los estados de sitios historicos de la BD
def get_all_states():
    return jsonify([x.json() for x in list_states()]), 201 

@historic_sites_bp.route('/logs/get-all/<int:id>', methods=['GET']) # Retorna todas los estados de sitios historicos de la BD
def get_all_logs(id):
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
    
    return jsonify(response), 201 

@historic_sites_bp.route('/tags/get-all', methods = ['GET'])
def __get_all_tags():
    tags = get_all_tags()

    return jsonify([x.json() for x in tags]), 201

@historic_sites_bp.route('/tags/site-tags/<int:id>', methods = ['GET'])
def __get_all_tags_by_site(id):
    list = get_tags_by_site(id)
    return jsonify([x.json() for x in list]), 201

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

