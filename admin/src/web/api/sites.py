from flask import Blueprint, jsonify, request, session
from src.core.models.review import list_reviews_with_filters, get_specific_review, create_review as create_review_model, update_data_review, remove_review
from src.core.models.historic_sites import list_historic_sites_with_advanced_filters, get_visible_historic_site, add_historic_site
from src.core.models.historic_site_tags import get_tag_by_name
from src.core.models.historic_sites_state.hs_states import HistoricSitesStates
from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.review.review import Review, ReviewStatus
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from src.core.models.auth import get_usuario_by_email
from flask_jwt_extended import jwt_required, get_jwt_identity

from datetime import datetime

sites_api = Blueprint('sites_api', __name__, url_prefix='/api/sites')

# ========================= SITIOS ========================

@sites_api.route('', methods=['GET'])

def get_historic_sites():
    """
    Obtiene los sitios históricos visibles con filtros avanzados y paginación.
    Query params:
        - name: string (optional) - Filtra por nombre (búsqueda parcial, case-insensitive)
        - description: string (optional) - Filtra por descripción (búsqueda parcial, case-insensitive)
        - city: string (optional) - Filtra por ciudad (búsqueda exacta, case-insensitive)
        - province: string (optional) - Filtra por provincia (búsqueda exacta, case-insensitive)
        - tags: string (optional) - Filtra por etiquetas (múltiples separadas por comas)
        - order_by: string (optional) - Ordena los resultados (default: latest)
        - lat: number (optional) - Latitud para búsqueda geoespacial
        - long: number (optional) - Longitud para búsqueda geoespacial
        - radius: number (optional) - Radio en kilómetros para búsqueda geoespacial (requiere lat y long)
        - page: number (optional) - Número de página (default: 1)
        - per_page: number (optional) - Cantidad de elementos por página (default: 20, max: 100)
    """
    try:
        # Parse parameters
        name = request.args.get('name')
        description = request.args.get('description')
        city = request.args.get('city')
        province = request.args.get('province')
        tags_str = request.args.get('tags')
        order_by = request.args.get('order_by', 'latest')
        lat_str = request.args.get('lat')
        long_str = request.args.get('long')
        radius_str = request.args.get('radius')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)
        
        # Validations
        if page < 1:
            return jsonify({"error": {"code": "invalid_query", "message": "Parameter validation failed", "details": {"page": ["Must be at least 1"]}}}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({"error": {"code": "invalid_query", "message": "Parameter validation failed", "details": {"per_page": ["Must be between 1 and 100"]}}}), 400
        if order_by not in ['rating-5-1', 'rating-1-5', 'latest', 'oldest']:
            return jsonify({"error": {"code": "invalid_query", "message": "Parameter validation failed", "details": {"order_by": ["Invalid choice"]}}}), 400
        
        # Parse geospatial parameters
        lat = None
        long = None
        radius = None
        if lat_str or long_str or radius_str:
            try:
                lat = float(lat_str) if lat_str else None
                long = float(long_str) if long_str else None
                radius = float(radius_str) if radius_str else None
            except ValueError:
                details = {}
                if lat_str: details["lat"] = ["Must be a number"]
                if long_str: details["long"] = ["Must be a number"]
                if radius_str: details["radius"] = ["Must be a number"]
                return jsonify({"error": {"code": "invalid_query", "message": "Parameter validation failed", "details": details}}), 400
            
            if lat is not None and not (-90 <= lat <= 90):
                return jsonify({"error": {"code": "invalid_query", "message": "Parameter validation failed", "details": {"lat": ["Must be a valid latitude"]}}}), 400
            if long is not None and not (-180 <= long <= 180):
                return jsonify({"error": {"code": "invalid_query", "message": "Parameter validation failed", "details": {"long": ["Must be a valid longitude"]}}}), 400
            if radius is not None and radius <= 0:
                return jsonify({"error": {"code": "invalid_query", "message": "Parameter validation failed", "details": {"radius": ["Must be positive"]}}}), 400
            if (lat is None or long is None) and radius is not None:
                return jsonify({"error": {"code": "invalid_query", "message": "Parameter validation failed", "details": {"radius": ["Requires lat and long"]}}}), 400
        
        # Parse tags
        tag_names = None
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        
        # Call service
        sites, total = list_historic_sites_with_advanced_filters(
            name=name,
            description=description,
            city=city,
            province=province,
            tag_names=tag_names,
            lat=lat,
            long=long,
            radius=radius,
            order_by=order_by,
            page=page,
            per_page=per_page
        )
        
        # Format response
        data = []
        for site in sites:
            data.append({
                "id": site.id,
                "name": site.site_name,
                "short_description": site.short_description,
                "description": site.long_description,
                "city": site.city,
                "province": site.province,
                "country": "AR",
                "lat": site.latitude,
                "long": site.longitude,
                "tags": [tag.name for tag in site.tags],
                "state_of_conservation": site.status.state,
                "inserted_at": site.registration_date.isoformat() + 'Z',
                "updated_at": site.registration_date.isoformat() + 'Z'  # Placeholder, as model doesn't have updated_at
            })
        
        return jsonify({
            "data": data,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": total
            }
        }), 200
    except Exception as e:
        return jsonify({"error": {"code": "server_error", "message": "An unexpected error occurred"}}), 500

@sites_api.route('/<int:site_id>', methods=['GET'])

def get_historic_site(site_id):
    """
    Obtiene detalles de un sitio histórico específico por su ID.
    No requiere autenticación.
    Example URI: historic-sites/10

    URI Parameters:
        - site_id: number (required) - ID del sitio histórico.

    Response 200:
        Headers: Content-Type: application/json
        Body: Ver schema en documentación.
    """
    try:
        site = get_visible_historic_site(site_id)
        if site:
            data = {
                "id": site.id,
                "name": site.site_name,
                "short_description": site.short_description,
                "description": site.long_description,
                "city": site.city,
                "province": site.province,
                "country": "AR",
                "lat": site.latitude,
                "long": site.longitude,
                "tags": [tag.name for tag in site.tags],
                "state_of_conservation": site.status.state,
                "inserted_at": site.registration_date.isoformat() + 'Z',
                "updated_at": site.registration_date.isoformat() + 'Z'  # Placeholder, as model doesn't have updated_at
            }
            return jsonify(data), 200
        else:
            return jsonify({"error": {"code": "not_found", "message": "Site not found"}}), 404
    except Exception as e:
        return jsonify({"error": {"code": "server_error", "message": "An unexpected error occurred"}}), 500


@sites_api.route('/<int:site_id>/reviews', methods=['GET'])

def get_historic_site_reviews(site_id):
    """
    Obtiene las reseñas aprobadas de un sitio histórico específico (público).
    Query params:
        - page: Número de página (default: 1)
        - per_page: Items por página (default: 10)
    Responde con el esquema { data: [...], meta: { page, per_page, total } }
    """
    try:
        # Validar que el sitio exista y sea visible
        site = get_visible_historic_site(site_id)
        if not site:
            return jsonify({"error": {"code": "not_found", "message": "Site not found"}}), 404

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Validaciones de paginación
        if page < 1:
            return jsonify({"error": {"code": "invalid_data", "message": "Invalid input data", "details": {"page": ["Must be at least 1"]}}}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({"error": {"code": "invalid_data", "message": "Invalid input data", "details": {"per_page": ["Must be between 1 and 100"]}}}), 400

        reviews, total = list_reviews_with_filters(
            site=site_id,
            status='APPROVED',
            page=page,
            per_page=per_page,
            order_by='inserted_at',
            order_dir='desc'
        )

        data = []
        for r in reviews:
            data.append({
                "id": r.id,
                "site_id": r.historic_site_id,
                "rating": r.rating,
                "comment": r.content,
                "user_name": f"{r.user.nombre} {r.user.apellido}",
                "inserted_at": r.inserted_at.isoformat() + 'Z' if hasattr(r, 'inserted_at') and r.inserted_at else None,
                "updated_at": r.updated_at.isoformat() + 'Z' if hasattr(r, 'updated_at') and r.updated_at else None,
            })

        return jsonify({
            "data": data,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": total
            }
        }), 200
    except Exception as e:
        return jsonify({"error": {"code": "server_error", "message": "An unexpected error occurred"}}), 500


@sites_api.route('/<int:site_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_historic_site_review(site_id, review_id):
    """
    Elimina una reseña específica de un sitio histórico.
    Solo el autor de la reseña puede eliminarla.
    Requiere autenticación vía JWT de Google en header Authorization.
    """
    try:
        # Verificar autenticación con JWT de Google
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": {"code": "unauthorized", "message": "Authentication required"}}), 401

        token = auth_header.split(' ')[1]
        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
            email = idinfo['email']
        except ValueError:
            return jsonify({"error": {"code": "unauthorized", "message": "Invalid token"}}), 401

        user = get_usuario_by_email(email)
        if not user or not user.activo:
            return jsonify({"error": {"code": "unauthorized", "message": "User not found or inactive"}}), 401

        # Verificar que el sitio existe
        site = get_visible_historic_site(site_id)
        if not site:
            return jsonify({"error": {"code": "not_found", "message": "Site not found"}}), 404

        # Verificar que la reseña existe y pertenece al sitio
        review = get_specific_review(review_id)
        if not review or review.historic_site_id != site_id:
            return jsonify({"error": {"code": "not_found", "message": "Review not found"}}), 404

        # Verificar que el usuario es el autor
        if review.user_id != user.id:
            return jsonify({"error": {"code": "forbidden", "message": "You do not have permission to delete this review"}}), 403

        # Eliminar la reseña
        if remove_review(review_id):
            return '', 204
        else:
            return jsonify({"error": {"code": "not_found", "message": "Review not found"}}), 404

    except Exception as e:
        return jsonify({"error": {"code": "server_error", "message": "An unexpected error occurred"}}), 500

# =============== Crear sitio =================

@sites_api.route('', methods=['POST'])
@jwt_required()
def create_historic_site():
    """
    Crea un nuevo sitio histórico.
    Requiere autenticación JWT.
    """
    try:
        # Obtener user_id del JWT token 
        user_id = get_jwt_identity()

        # Validar que se envió JSON
        if not request.is_json:
            return jsonify({"error": {"code": "invalid_data", "message": "Invalid input data", "details": {"content-type": ["Must be application/json"]}}}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": {"code": "invalid_data", "message": "Invalid input data", "details": {"body": ["Request body is required"]}}}), 400

        # Validar campos requeridos
        required_fields = ['name', 'short_description', 'description', 'city', 'province', 'lat', 'long', 'state_of_conservation']
        validation_errors = {}
        
        for field in required_fields:
            if field not in data or not data[field]:
                validation_errors[field] = ["This field is required"]

        # Validar tipos de datos
        if 'lat' in data:
            try:
                lat = float(data['lat'])
                if not (-90 <= lat <= 90):
                    validation_errors['lat'] = ["Must be a valid latitude between -90 and 90"]
            except (ValueError, TypeError):
                validation_errors['lat'] = ["Must be a number"]

        if 'long' in data:
            try:
                long_val = float(data['long'])
                if not (-180 <= long_val <= 180):
                    validation_errors['long'] = ["Must be a valid longitude between -180 and 180"]
            except (ValueError, TypeError):
                validation_errors['long'] = ["Must be a number"]

        # Validar estado de conservación
        if 'state_of_conservation' in data:
            valid_states = ['excelente', 'bueno', 'regular', 'malo']
            if data['state_of_conservation'] not in valid_states:
                validation_errors['state_of_conservation'] = [f"Must be one of: {', '.join(valid_states)}"]

        if validation_errors:
            return jsonify({"error": {"code": "invalid_data", "message": "Invalid input data", "details": validation_errors}}), 400

        # Procesar tags
        tag_names = data.get('tags', [])
        tag_ids = []
        
        if tag_names:
            for tag_name in tag_names:
                tag = get_tag_by_name(tag_name)
                tag_ids.append(tag.id)

        # Obtener estado de conservación por nombre
        estado = db.session.query(HistoricSitesStates).filter_by(state=data['state_of_conservation']).first()
        if not estado:
            return jsonify({"error": {"code": "invalid_data", "message": "Invalid state_of_conservation"}}), 400

        # Obtener categoría por defecto 
        categoria = db.session.query(HistoricSitesCategories).first()
        if not categoria:
            return jsonify({"error": {"code": "server_error", "message": "No categories available"}}), 500

        # Crear sitio histórico
        site = add_historic_site(
            site_name=data['name'],
            short_description=data['short_description'],
            long_description=data['description'],
            city=data['city'],
            province=data['province'],
            latitude=float(data['lat']),
            longitude=float(data['long']),
            conservation_status=estado.id,
            inauguration_year=datetime.now(),  # O se podría agregar al request
            category=categoria.id,
            user_id=user_id,
            visible=False,  # Los sitios creados por usuarios públicos están ocultos por defecto
            tags=tag_ids,
            country=data.get('country', 'AR')  
        )

        # Formatear respuesta según especificación
        response_data = {
            "id": site.id,
            "name": site.site_name,
            "short_description": site.short_description,
            "description": site.long_description,
            "city": site.city,
            "province": site.province,
            "country": data.get('country', 'AR'),
            "lat": site.latitude,
            "long": site.longitude,
            "tags": [tag_name for tag_name in tag_names],
            "state_of_conservation": data['state_of_conservation'],
            "inserted_at": site.registration_date.isoformat() + 'Z',
            "updated_at": site.registration_date.isoformat() + 'Z',
            "user_id": user_id
        }

        return jsonify(response_data), 201

    except SQLAlchemyError as e:
        return jsonify({"error": {"code": "server_error", "message": "Database error"}}), 500
    except Exception as e:
        return jsonify({"error": {"code": "server_error", "message": "An unexpected error occurred"}}), 500
