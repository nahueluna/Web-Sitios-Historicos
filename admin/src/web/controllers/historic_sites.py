from os import abort
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, Response
from src.core.models.historic_sites import get_historic_site, list_all_historic_sites, list_visible_historic_sites, add_historic_site, edit_historic_site
from src.core.models.historic_sites_categorie import list_historic_sites_categorie, add_category
from src.core.models.historic_sites_state import list_states
from src.core.models.historic_sites_logs import add_log, get_logs_per_hs
import pickle
import io, csv

historic_sites_bp = Blueprint('historic_sites', __name__, url_prefix='/sitios-historicos')

# -- USUAIROS -- #

# RENDERING
@historic_sites_bp.route('/') # Renderiza html
def render_index(): return render_template('/historic_sites/index.html')

@historic_sites_bp.route('/detalle/<int:id>') # Renderiza html
def render_detail(id): return render_template('historic_sites/historic_site_detail.html')
# RENDERING

@historic_sites_bp.route('/get-all', methods=['GET']) # Retorna todos los sitios historicos de la BD
def get_all(): 
    # PREGUNTAR SESION PARA MOSTRATR TODOS O SOLO VISIBLES
    json = [x.json() for x in list_visible_historic_sites()]
    return jsonify(json), 201


# Endpoint para generar CSV del lado del servidor
@historic_sites_bp.route('/export-sites', methods=['GET'])
def export_sites():
    data = [x.json() for x in list_all_historic_sites()]
    
    # Devolver si no hay sitios
    if len(data) == 0:
        return jsonify({"error": "No hay datos para exportar"}), 404

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

    fieldnames = list(column_translation.values()) + ["Coordenadas de geolocalizacion"]

    # StringIO sirve para crear un archivo en memoria, en este caso CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=",")
    writer.writeheader()

    for row in data:
        # Creo una nueva fila
        spanish_row = {}
        
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
def get_site(id):
    hs = get_historic_site(int(id))
    response = {
        "historic_site": hs[0].json(),
        "category": hs[1].category,
        "state": hs[2].state
    }
    return jsonify(response), 201

# -- USUAIROS -- #

# -- ADMIN -- #

# RENDERING
@historic_sites_bp.route('/admin/gestion-sitios')  # Renderiza html
def render_admin_management(): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('/historic_sites/gestion_sitios.html')

@historic_sites_bp.route('/admin/')  # Renderiza html
def render_admin_sites(): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('/historic_sites/index.html')

@historic_sites_bp.route('/admin/agregar-sitio') # 
def render_site_form(): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('historic_sites/add_historic_site.html')

@historic_sites_bp.route('/admin/editar-sitio/<int:id>') # 
def render_edite_site_form(id): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('historic_sites/edit_historic_site.html')

@historic_sites_bp.route('/admin/categorias') # 
def render_admin_categories(): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('historic_sites/category/categories.html')

@historic_sites_bp.route('/admin/categorias/agregar') # 
def render_category_form(): 
    # PREGUNTAR SI TIENE PERMISIOS
    return render_template('historic_sites/category/add_category.html')

# RENDERING

@historic_sites_bp.route('/add-site', methods=['POST']) # 
def add_site(): 
    json = request.get_json()
    
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
    )

    add_log(hs_id=hs.id, action_type="Creación") # AGREGAR EL USUARIO INVOLUCRADO (ID)

    return jsonify({}), 201

@historic_sites_bp.route('/edit-site', methods=['PUT'])
def edit_site(): 
    json = request.get_json()
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
    )

    add_log(hs_id=int(json['id']), action_type="Edición") # AGREGAR EL USUARIO INVOLUCRADO (ID)

    return jsonify({}), 201

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
    return jsonify([x.json() for x in get_logs_per_hs(hs_id=id)]), 201 

# -- AUXILIARES -- #

__hs_labels__ = ["Etiqueta 1", "Etiqueta 2", "Etiqueta 3"]