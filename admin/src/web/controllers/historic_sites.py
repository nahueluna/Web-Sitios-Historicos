from os import abort
from flask import Blueprint, render_template, request 

historic_sites_bp = Blueprint('historic_sites', __name__, url_prefix='/sitios-historicos')

# -- USUAIROS -- #

@historic_sites_bp.route('/', methods=['GET']) # Retorna todos los sitios historicos de la BD
def list_historic_sites(): return render_template('/historic_sites/index.html', list=__hs__)

@historic_sites_bp.route('/detalle/<int:id>', methods=['GET', 'POST'])
def view_historic_site(id):
    if request.method == 'POST':

        json = request.form.to_dict()

        hs = {
            "site-name": json.get("site-name"),
            "short-description": json.get("short-description"),
            "long-description": json.get("long-description"),
            "city": json.get("city"),
            "province": json.get("province"),
            "geographic-location": {
                "latitude": json.get("latitude"),
                "longitude": json.get("longitude")
            },
            "conservation-status": json.get("conservation-status"),
            "inauguration-year": json.get("inauguration-year"),
            "category": json.get("category"),
            "registration-date": json.get("registration-date"),
            "visible": json.get("visible")
        }
        print(hs)

        # INSTANCIAR CLASE DE SQLACHEMY Y LLAMAR A MÉTODO PARA GUARDAR EN BD
        hs["id"] = len(__hs__) + 1  # Simulando la asignación de un ID
        __hs__.append(hs)  # Simulando la inserción en la base de datos

        return render_template('historic_sites/historic_site_detail.html', historic_site=hs)
    
    elif request.method == 'GET':
        
        # LLAMAR A MÉTODO PARA OBTENER EL SITIO HISTÓRICO DE LA
        # LLAMAR AL METODO DE LA CLASE DE SQLACHEMY PARA QUE DEVUELTA EL HS
        hs = __hs__[id-1] # Simulando la obtención del sitio histórico por ID

        return render_template('historic_sites/historic_site_detail.html', historic_site=hs)
    else:
        #return "Method Not Allowed", 404
        abort(404)

# -- USUAIROS -- #

# -- ADMIN -- #

@historic_sites_bp.route('/admin', methods=['GET']) # Agregar sitios historicos, agregar Categorias
def admin_historic_sites(): return render_template('/historic_sites/gestion_sitios.html', list=__hs__)

@historic_sites_bp.route('/admin/agregar-categoria', methods=['GET']) # Renderiza un formulario para agregar una nueva categoria
def add_categorie(): return render_template('historic_sites/add_categorie.html')

@historic_sites_bp.route('/admin/agregar-sitio', methods=['GET']) # Renderiza un formulario para agregar un nuevo sitio histórico
def add_historic_site(): return render_template('historic_sites/add_historic_site.html', states=__hs_states__)

@historic_sites_bp.route('/admin/editar-sitio/<int:id>', methods=['GET']) # Renderiza un formulario para editar un sitio histórico
def edit_historic_site(id): 
    return render_template('/historic_sites/edit_historic_site.html', historic_site=__hs__[id-1], states=__hs_states__)

# -- ADMIN -- #

__hs__ = [
    {   
        "id": 1,
        "site-name": "Historic Site Example",
        "short-description": "A brief description of the historic site.",
        "long-description": "Location details",
        "city": "City Name",
        "province": "Province Name",
        "geographic-location": { "latitude": 123, "longitude": 456 },
        "conservation-status": "Bueno",
        "inauguration-year": 1900,
        "category": "Category Name",
        "registration-date": "2023-01-01",
        "visible": True
    },
    {
        "id": 2,
        "site-name": "Historic Site Example",
        "short-description": "A brief description of the historic site.",
        "long-description": "Location details",
        "city": "City Name",
        "province": "Province Name",
        "geographic-location": { "latitude": 123, "longitude": 456 },
        "conservation-status": "Regular",
        "inauguration-year": 1900,
        "category": "Category Name",
        "registration-date": "2023-01-01",
        "visible": True
    },
    {
        "id": 3,
        "site-name": "Historic Site Example",
        "short-description": "A brief description of the historic site.",
        "long-description": "Location details",
        "city": "City Name",
        "province": "Province Name",
        "geographic-location": { "latitude": 123, "longitude": 456 },
        "conservation-status": "Malo",
        "inauguration-year": 1900,
        "category": "Category Name",
        "registration-date": "2023-01-01",
        "visible": True
    }
]

__hs_states__ = ["Bueno", "Regular", "Malo"]

__hs_labels__ = ["Etiqueta 1", "Etiqueta 2", "Etiqueta 3"]