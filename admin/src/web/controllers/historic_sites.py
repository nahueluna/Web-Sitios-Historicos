from os import abort
from flask import Blueprint, render_template, request 
from src.core.models import historic_sites, historic_sites_state, historic_sites_categorie

from src.core.models.historic_sites_state import list_historic_sites_states
from src.core.models.historic_sites_categorie import list_historic_sites_categorie

historic_sites_bp = Blueprint('historic_sites', __name__, url_prefix='/sitios-historicos')

# -- USUAIROS -- #

@historic_sites_bp.route('/', methods=['GET']) # Retorna todos los sitios historicos de la BD
def list_historic_sites(): return render_template('/historic_sites/index.html', list= historic_sites.list_visible_historic_sites())

@historic_sites_bp.route('/detalle/<int:id>', methods=['GET', 'POST'])
def view_historic_site(id):
    if request.method == 'POST':

        json = request.form.to_dict()

        hs = historic_sites.add_historic_site(
            site_name= json.get("site-name"),
            short_description= json.get("short-description"),
            long_description= json.get("long-description"),
            city= json.get("city"),
            province= json.get("province"),
            latitude= json.get("latitude"),
            longitude= json.get("longitude"),
            conservation_status= json.get("conservation-status"),
            inauguration_year= json.get("inauguration-year"),
            category= json.get("category"),
            visible= bool(json.get("visible"))
        )

        return render_template('historic_sites/historic_site_detail.html', historic_site=hs)
    
    elif request.method == 'GET':
        
        hs = historic_sites.get_historic_site(id)
        return render_template('historic_sites/historic_site_detail.html', historic_site=hs)
    else:
        #return "Method Not Allowed", 404
        abort(404)

# -- USUAIROS -- #

# -- ADMIN -- #

@historic_sites_bp.route('/admin', methods=['GET']) # Agregar sitios historicos, agregar Categorias
def admin_historic_sites(): return render_template('/historic_sites/gestion_sitios.html', list=historic_sites.list_all_historic_sites())

@historic_sites_bp.route('/admin/agregar-categoria', methods=['GET']) # Renderiza un formulario para agregar una nueva categoria
def add_categorie(): return render_template('historic_sites/add_categorie.html')

@historic_sites_bp.route('/admin/agregar-sitio', methods=['GET']) # Renderiza un formulario para agregar un nuevo sitio histórico
def add_historic_site(): 
    return render_template(
        'historic_sites/add_historic_site.html', 
        states=historic_sites_state.list_historic_sites_states(), 
        categories=historic_sites_categorie.list_historic_sites_categorie()
        )

@historic_sites_bp.route('/admin/editar-sitio/<int:id>', methods=['GET']) # Renderiza un formulario para editar un sitio histórico
def edit_historic_site(id): 
    return render_template(
        '/historic_sites/edit_historic_site.html', 
        historic_site=historic_sites.get_historic_site(id), 
        states=historic_sites_state.list_historic_sites_states(), 
        categories=historic_sites_categorie.list_historic_sites_categorie()
        )

# -- ADMIN -- #


__hs_labels__ = ["Etiqueta 1", "Etiqueta 2", "Etiqueta 3"]