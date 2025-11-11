from flask import Blueprint, request, jsonify, session, current_app
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from core.models.historic_sites import public_list_historic_sites
from src.web.handlers.auth import is_authenticated
from src.core.models.auth import get_usuario_by_email

# Blueprint para api publica
public_api_bp = Blueprint('public_api', __name__, url_prefix='/api')

@public_api_bp.post('/auth')
def generate_jwt_token():
    if not is_authenticated():
        return jsonify({"error": {
            "code": "invalid_credentials",
            "message": "Credenciales inválidas."
        }}), 401
    
    user = get_usuario_by_email(session["user"])
    if not user:
        # Para en caso de sesiones truchas? ns
        return jsonify({"error": {
            "code": "invalid_credentials",
            "message": "Credenciales inválidas."
        }}), 401
    
    if not user.activo:
        return jsonify({"error": {
            "code": "access_denied",
            "message": "Credenciales no corresponden a un usuario activo."
        }}), 403
    
    # Crear token 
    access_token = create_access_token(identity=user.id)
    
    # Obtener tiempo en segundos de expiracion desde la configuracion
    expires_delta = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
    total_seconds = int(expires_delta.total_seconds())
    
    return jsonify({
        "token": access_token,
        "expires_in": total_seconds
    }), 200

@public_api_bp.get('/sites') # No requiere autenticación
def get_public_historic_sites():
    
    def validate_params():
        # Validar parametros de entrada
        errors = {}
        
        # Validar lat y long
        lat = request.args.get('lat')
        long = request.args.get('long')
        radius = request.args.get('radius')
        
        if lat is not None:
            try:
                lat_val = float(lat)
                if not (-90 <= lat_val <= 90):
                    errors['lat'] = ["Must be a valid latitude between -90 and 90"]
            except ValueError:
                errors['lat'] = ["Must be a valid latitude"]
        
        if long is not None:
            try:
                long_val = float(long)
                if not (-180 <= long_val <= 180):
                    errors['long'] = ["Must be a valid longitude between -180 and 180"]
            except ValueError:
                errors['long'] = ["Must be a valid longitude"]
        
        # Validar que si hay radius, también hay lat y long
        if radius is not None and (lat is None or long is None):
            if 'lat' not in errors:
                errors['lat'] = []
            if 'long' not in errors:
                errors['long'] = []
            errors['lat'].append("Required when radius is provided")
            errors['long'].append("Required when radius is provided")
        
        # Validar per_page
        per_page = request.args.get('per_page')
        if per_page is not None:
            try:
                per_page_val = int(per_page)
                if not (1 <= per_page_val <= 100):
                    errors['per_page'] = ["Must be between 1 and 100"]
            except ValueError:
                errors['per_page'] = ["Must be a valid number"]
        
        # Validar page
        page = request.args.get('page')
        if page is not None:
            try:
                page_val = int(page)
                if page_val < 1:
                    errors['page'] = ["Must be at least 1"]
            except ValueError:
                errors['page'] = ["Must be a valid number"]
        
        # Validar order_by
        order_by = request.args.get('order_by')
        if order_by is not None and order_by not in ['rating-5-1', 'rating-1-5', 'latest', 'oldest']:
            errors['order_by'] = ["Must be one of: rating-5-1, rating-1-5, latest, oldest"]
        
        return errors

    # Validar parámetros
    validation_errors = validate_params()
    if validation_errors:
        response = jsonify({
            "error": {
                "code": "invalid_query", 
                "message": "Parameter validation failed",
                "details": validation_errors
            }
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 400

    try:
        # Extraer y procesar parámetros
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        city = request.args.get('city', '')
        province = request.args.get('province', '')
        order_by = request.args.get('order_by', 'latest')
        
        # Parámetros numéricos
        lat = request.args.get('lat', type=float)
        long = request.args.get('long', type=float) 
        radius = request.args.get('radius', type=float)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Procesar tags
        tags = request.args.get('tags')
        if tags:
            tags = [tag.strip() for tag in tags.split(',')]
        else:
            tags = None

        # Llamar a la función específica para obtener los sitios
        (sites, total) = public_list_historic_sites(
            name=name,
            description=description,
            city=city,
            province=province,
            tags=tags,
            order_by=order_by,
            lat=lat,
            long=long,
            radius=radius,
            page=page,
            per_page=per_page
        )

        # Formatear respuesta según especificación
        data = []
        for site in sites:
            site_data = {
                "id": site.id,
                "name": site.site_name,
                "short_description": site.short_description,
                "description": site.long_description,
                "city": site.city,
                "province": site.province,
                "country": site.country,
                "lat": site.latitude,
                "long": site.longitude,
                "tags": [tag.name for tag in site.tags],
                "average_rating": site.average_rating, 
                "state_of_conservation": site.conservation_status if hasattr(site, 'conservation_status') else "unknown",
                "inserted_at": site.registration_date.isoformat() + "Z" if site.registration_date else None,
                "updated_at": site.registration_date.isoformat() + "Z" if site.registration_date else None  # TODO: Implementar updated_at
            }
            data.append(site_data)

        response_data = {
            "data": data,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": total
            }
        }

        response = jsonify(response_data)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 200

    except Exception as e:
        print("-------------------ERROR--------------", e)
        response = jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 500