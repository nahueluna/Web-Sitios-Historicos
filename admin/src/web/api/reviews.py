from flask import Blueprint, jsonify, request, session
from src.core.models.review import list_reviews_with_filters, get_specific_review, create_review as create_review_model, update_data_review, remove_review
from src.core.models.historic_sites import list_historic_sites_with_advanced_filters, get_visible_historic_site
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.review.review import Review, ReviewStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from src.web.decorator import block_portal_maintenance, require_feature
from src.web.schemas.review import (
    ReviewCreateSchema,
    ReviewUpdateSchema, 
    ReviewSearchSchema,
    UserReviewsSearchSchema
)

reviews_api = Blueprint('reviews_api', __name__, url_prefix='/api/reviews')

# ========================= RESEÑAS ========================

# Conseguir reviews aprobadas
@reviews_api.route('', methods=['GET'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
def get_approved_reviews():
    try:
        search_schema = ReviewSearchSchema()
        try:
            query_params = search_schema.load(request.args)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "invalid_query",
                    "message": "Parameter validation failed",
                    "details": err.messages
                }
            }), 400
        
        site_id = query_params.get('site')
        page = query_params['page']
        per_page = query_params['per_page']
        
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

# Conseguir review por id
@reviews_api.route('/<int:review_id>', methods=['GET'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
def get_review(review_id):
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

# Actualizar review 
@reviews_api.route('/<int:review_id>', methods=['PUT'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
def update_review(review_id):
    try:
        user_id = get_jwt_identity()

        # Verificar que la reseña existe y es del usuario
        review = get_specific_review(review_id)
        if not review:
            return jsonify({"error": "Reseña no encontrada"}), 404

        if review.user_id != user_id:
            return jsonify({"error": {"code": "forbidden", "message": "Solo puedes actualizar tus propias reseñas"}}), 403

        update_schema = ReviewUpdateSchema()
        try:
            data = update_schema.load(request.json)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "validation_failed",
                    "message": "Data validation failed",
                    "details": err.messages
                }
            }), 400

        content = data.get('content')
        rating = data['rating']

        review = update_data_review(review_id, rating=rating, content=content)
        if review:
            return jsonify({"message": "Reseña actualizada exitosamente", "review": review.json()}), 200
        else:
            return jsonify({"error": "Reseña no encontrada"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": "Error al actualizar la reseña", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

# Crear nueva review
@reviews_api.route('/', methods=['POST'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
def create_review():
    try:
        user_id = get_jwt_identity()

        create_schema = ReviewCreateSchema()
        try:
            data = create_schema.load(request.json)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "validation_failed",
                    "message": "Data validation failed",
                    "details": err.messages
                }
            }), 400
        
        # Crear reseña con user_id del usuario autenticado
        review_data = {
            'content': data['content'],
            'rating': data['rating'],
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
    
# Conseguir reviews de un usuario
@reviews_api.route('/users/<int:user_id>/reviews', methods=['GET'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
def get_user_reviews(user_id):
    try:
        search_schema = UserReviewsSearchSchema()
        try:
            query_params = search_schema.load(request.args)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "invalid_query",
                    "message": "Parameter validation failed",
                    "details": err.messages
                }
            }), 400
        
        page = query_params['page']
        per_page = query_params['per_page']
        
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