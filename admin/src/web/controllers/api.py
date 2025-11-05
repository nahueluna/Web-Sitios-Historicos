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

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ========================= RESEÑAS ========================

@api_bp.route('/reviews', methods=['GET'])
def get_approved_reviews():
    """
    Obtiene reseñas aprobadas con filtros opcionales.
    Query params:
        - site: ID del sitio histórico
        - page: Número de página (default: 1)
        - per_page: Items por página (default: 25)
    """
    try:
        site_id = request.args.get('site')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)
        
        # Validar paginación
        if page < 1:
            return jsonify({"error": "El número de página debe ser mayor a 0"}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({"error": "per_page debe estar entre 1 y 100"}), 400
        
        reviews, total = list_reviews_with_filters(
            site=site_id, 
            status='APPROVED',
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            "reviews": [review.json() for review in reviews],
            "total": total,
            "page": page,
            "per_page": per_page
        }), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener las reseñas", "details": str(e)}), 500

@api_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """
    Obtiene el detalle de una reseña específica por ID.
    Solo devuelve reseñas aprobadas.
    """
    try:
        review = get_specific_review(review_id)
        if review:
            # Validar que sea una reseña aprobada (público solo ve aprobadas)
            if review.status.name != 'APPROVED':
                return jsonify({"error": "Reseña no encontrada"}), 404
            return jsonify(review.json()), 200
        else:
            return jsonify({"error": "Reseña no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener la reseña", "details": str(e)}), 500

@api_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Actualiza el contenido y/o rating de una reseña.
    Solo el autor de la reseña puede actualizarla.
    Requiere autenticación vía JWT de Google en header Authorization.
    Body JSON:
        - content: Contenido de la reseña (opcional)
        - rating: Calificación 1-5 (requerido)
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

        # Verificar que la reseña existe y es del usuario
        review = get_specific_review(review_id)
        if not review:
            return jsonify({"error": "Reseña no encontrada"}), 404

        if review.user_id != user.id:
            return jsonify({"error": {"code": "forbidden", "message": "You can only update your own reviews"}}), 403

        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        content = data.get('content')
        rating = data.get('rating')

        # Validaciones
        if rating is None:
            return jsonify({"error": "El rating es obligatorio"}), 400
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({"error": "El rating debe estar entre 1 y 5"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "El rating debe ser un número entero"}), 400
        
        if content and len(content) > 1000:
            return jsonify({"error": "El contenido no puede exceder 1000 caracteres"}), 400

        review = update_data_review(review_id, rating=rating, content=content)
        if review:
            return jsonify({"message": "Reseña actualizada exitosamente", "review": review.json()}), 200
        else:
            return jsonify({"error": "Reseña no encontrada"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": "Error al actualizar la reseña", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

@api_bp.route('/reviews', methods=['POST'])
def create_review():
    """
    Crea una nueva reseña.
    Requiere autenticación vía JWT de Google en header Authorization.
    Body JSON:
        - content: Contenido de la reseña (requerido)
        - rating: Calificación 1-5 (requerido)
        - historic_site_id: ID del sitio histórico (requerido)
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

        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        # Validar campos requeridos
        required_fields = ['content', 'rating', 'historic_site_id']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": "Faltan campos obligatorios",
                "missing_fields": missing_fields
            }), 400
        
        # Validar rating
        try:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                return jsonify({"error": "El rating debe estar entre 1 y 5"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "El rating debe ser un número entero"}), 400
        
        # Validar longitud del contenido
        if len(data['content']) > 1000:
            return jsonify({"error": "El contenido no puede exceder 1000 caracteres"}), 400
        
        if not data['content'].strip():
            return jsonify({"error": "El contenido no puede estar vacío"}), 400
        
        # Crear reseña con user_id del usuario autenticado
        review_data = {
            'content': data['content'],
            'rating': rating,
            'historic_site_id': data['historic_site_id'],
            'user_id': user.id
        }
        
        review = create_review_model(**review_data)
        return jsonify({
            "message": "Reseña creada exitosamente. Será revisada por un moderador.",
            "review": review.json()
        }), 201
    except SQLAlchemyError as e:
        error_msg = str(e)
        # Detectar violación de constraint único (usuario ya reseñó este sitio)
        if 'uq_historic_site_and_user' in error_msg or 'UNIQUE constraint' in error_msg:
            return jsonify({"error": "Ya has creado una reseña para este sitio histórico"}), 409
        return jsonify({"error": "Error al crear la reseña", "details": error_msg}), 500
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500
    

@api_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    """
    Obtiene las reseñas aprobadas de un usuario específico (para su perfil público).
    Solo devuelve reseñas con estado APPROVED.
    
    Query params:
        - page: Número de página (default: 1)
        - per_page: Items por página (default: 25)
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)
        
        # Validar paginación
        if page < 1:
            return jsonify({"error": "El número de página debe ser mayor a 0"}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({"error": "per_page debe estar entre 1 y 100"}), 400
        
        # Siempre filtrar por APPROVED (API pública)
        reviews, total = list_reviews_with_filters(
            user_id=user_id,
            status='APPROVED',
            page=page,
            per_page=per_page,
            order_by='inserted_at',
            order_dir='desc'
        )
        
        return jsonify({
            "reviews": [review.json() for review in reviews],
            "total": total,
            "page": page,
            "per_page": per_page,
            "user_id": user_id
        }), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener las reseñas del usuario", "details": str(e)}), 500


# ========================= SITIOS ========================

@api_bp.route('/historic-sites', methods=['GET'])
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


@api_bp.route('/historic-sites/<int:site_id>', methods=['GET'])
def get_historic_site(site_id):
    """
    Obtiene el detalle de un sitio histórico específico por ID.
    Solo devuelve sitios visibles.
    """
    try:
        site = get_visible_historic_site(site_id)
        if site:
            return jsonify(site.json()), 200
        else:
            return jsonify({"error": "Sitio histórico no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener el sitio histórico", "details": str(e)}), 500


@api_bp.route('/historic-sites/<int:site_id>/reviews', methods=['GET'])
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


@api_bp.route('/historic-sites/<int:site_id>/reviews/<int:review_id>', methods=['DELETE'])
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
