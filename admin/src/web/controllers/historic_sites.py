from flask import Blueprint, render_template, request 

historyc_sites_bp = Blueprint('historic_sites', __name__, url_prefix='/sitios-historicos')

@historyc_sites_bp.route('/', methods=['GET']) # Retorna todos los sitios historicos de la BD
def list_historic_sites(): return render_template('/historic_sites/index.html')

@historyc_sites_bp.route('/agregar', methods=['GET']) # Renderiza un formulario para agregar un nuevo sitio histórico
def add_historic_site(): return render_template('historic_sites/add_historic_site.html')

@historyc_sites_bp.route('/detalle/<int:id>', methods=['GET', 'POST'])
def view_historic_site(id):
    if request.method == 'POST':
        json = request.get_json()
        hs = {
            "site-name": json.get("site-name"),
            "short-description": json.get("short-description"),
            "long-description": json.get("long-description"),
            "city": json.get("city"),
            "province": json.get("province"),
            "geographic-location": {
                "latitude": json.get("geographic-location", {}).get("latitude"),
                "longitude": json.get("geographic-location", {}).get("longitude")
            },
            "conservation-status": json.get("conservation-status"),
            "inauguration-year": json.get("inauguration-year"),
            "category": json.get("category"),
            "registration-date": json.get("registration-date"),
            "visible": json.get("visible")
        }

        # INSTANCIAR CLASE DE SQLACHEMY Y LLAMAR A MÉTODO PARA GUARDAR EN BD

        return render_template('historic_sites/historic_site_detail.html', historyc_site=hs)
    
    elif request.method == 'GET':
        
        # LLAMAR A MÉTODO PARA OBTENER EL SITIO HISTÓRICO DE LA
        # LLAMAR AL METODO DE LA CLASE DE SQLACHEMY PARA QUE DEVUELTA EL HS

        hs = {
            "site-name": "Historic Site Example",
            "short-description": "A brief description of the historic site.",
            "long-description": "Location details",
            "city": "City Name",
            "province": "Province Name",
            "geographic-location": { "latitude": 123, "longitude": 456 },
            "conservation-status": "Good",
            "inauguration-year": 1900,
            "category": "Category Name",
            "registration-date": "2023-01-01",
            "visible": True
        }
        return render_template('historic_sites/historic_site_detail.html', historyc_site=hs)
    else:
        return "Method Not Allowed", 404
