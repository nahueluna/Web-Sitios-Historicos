from flask import Blueprint, jsonify, request, session
from src.core.models.review import list_reviews_with_filters, get_specific_review, create_review as create_review_model, update_data_review, remove_review
from src.core.models.historic_sites import list_historic_sites_with_advanced_filters, get_visible_historic_site
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.review.review import Review, ReviewStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.web.decorator import block_portal_maintenance, require_feature

reviews_api = Blueprint('reviews_api', __name__, url_prefix='/api/reviews')

# ========================= RESEÑAS ========================

@reviews_api.route('', methods=['GET'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
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

@reviews_api.route('/<int:review_id>', methods=['GET'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
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

@reviews_api.route('/<int:review_id>', methods=['PUT'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
def update_review(review_id):
    """
    Actualiza el contenido y/o rating de una reseña.
    Solo el autor de la reseña puede actualizarla.
    Requiere autenticación JWT.
    Body JSON:
        - content: Contenido de la reseña (opcional)
        - rating: Calificación 1-5 (requerido)
    """
    try:
        user_id = get_jwt_identity()

        # Verificar que la reseña existe y es del usuario
        review = get_specific_review(review_id)
        if not review:
            return jsonify({"error": "Reseña no encontrada"}), 404

        if review.user_id != user_id:
            return jsonify({"error": {"code": "forbidden", "message": "Solo puedes actualizar tus propias reseñas"}}), 403

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

@reviews_api.route('/', methods=['POST'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
def create_review():
    """
    Crea una nueva reseña.
    Requiere autenticación JWT.
    Body JSON:
        - content: Contenido de la reseña (requerido)
        - rating: Calificación 1-5 (requerido)
        - historic_site_id: ID del sitio histórico (requerido)
    """
    try:
        user_id = get_jwt_identity()

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
            'user_id': user_id
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
    

@reviews_api.route('/users/<int:user_id>/reviews', methods=['GET'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
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