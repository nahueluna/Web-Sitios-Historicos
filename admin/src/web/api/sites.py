from flask import Blueprint, jsonify, request, session
from src.core.models.review import list_reviews_with_filters, get_specific_review, create_review as create_review_model, update_data_review, remove_review
from src.core.models.historic_sites import list_historic_sites_with_advanced_filters, get_visible_historic_site
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.review.review import Review, ReviewStatus
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from src.core.models.auth import get_usuario_by_email
from flask_jwt_extended import jwt_required

sites_api = Blueprint('sites_api', __name__, url_prefix='/api/historic-sites')

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
