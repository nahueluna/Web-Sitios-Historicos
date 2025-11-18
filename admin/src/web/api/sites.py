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
from src.core.models.images import get_thumbnail, get_images_by_site
from src.core.models.review.review import Review, ReviewStatus
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from src.core.models.auth import get_usuario_by_email
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime
from src.web.decorator import block_portal_maintenance, require_feature

from src.web.schemas.sites import (
    HistoricSiteSearchSchema,
    HistoricSiteCreateSchema,
)
from src.web.schemas.review import (
    ReviewCreateSchema,
    ReviewUpdateSchema,
)

sites_api = Blueprint('sites_api', __name__, url_prefix='/api/sites')

# ========================= SITIOS ========================

@sites_api.route('', methods=['GET'])
@block_portal_maintenance
def get_historic_sites():
    try:
        # Cargo el schema y los parametros, marshmallow se encarga de cargar los errores si los hay
        search_schema = HistoricSiteSearchSchema()
        try:
            query_params = search_schema.load(request.args)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "invalid_query",
                    "message": "Error al validar los parámetros",
                    "details": err.messages
                }
            }), 400

        name = query_params.get('name')
        description = query_params.get('description')
        city = query_params.get('city')
        province = query_params.get('province')
        tags_str = query_params.get('tags')
        order_by = query_params['order_by']
        lat = query_params.get('lat')
        long = query_params.get('long')
        radius = query_params.get('radius')
        page = query_params['page']
        per_page = query_params['per_page']

        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()] if tags_str else []

        # Tira error si no hay lat y long
        if radius is not None and (lat is None or long is None):
            return jsonify({
                "error": {
                    "code": "invalid_query",
                    "message": "Error al validar los parámetros",
                    "details": {"radius": ["Requiere latitud y longitud"]}
                }
            }), 400

        sites, total = list_historic_sites_with_advanced_filters(
            name=name,
            description=description,
            city=city,
            province=province,
            tag_names=tags, 
            lat=lat,
            long=long,
            radius=radius,
            order_by=order_by,
            page=page,
            per_page=per_page
        )

        data = []
        for site in sites:
            thumbnail = get_thumbnail(site.id)
            site_data = {
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
                "thumbnail_url": thumbnail.url if thumbnail else None,
                "thumbnail_alt": thumbnail.titulo if thumbnail else None
            }
            data.append(site_data)
        
        return jsonify({
            "data": data,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": total
            }
        }), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": {"code": "server_error", "message": "Ocurrió un error inesperado"}}), 500

@sites_api.route('/<int:site_id>', methods=['GET'])
@block_portal_maintenance
def get_historic_site(site_id):
    try:
        site = get_visible_historic_site(site_id)
        if site:
            images = get_images_by_site(site_id)
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
                "images": [image.json() for image in images],
            }
            return jsonify(data), 200
        else:
            return jsonify({"error": {"code": "not_found", "message": "Site not found"}}), 404
    except Exception as e:
        return jsonify({"error": {"code": "server_error", "message": "An unexpected error occurred"}}), 500


@sites_api.route('/<int:site_id>/reviews', methods=['GET'])
@block_portal_maintenance
@require_feature('reviews_enabled')
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
                "content": r.content,
                "user_name": f"{r.user.nombre} {r.user.apellido}",
                "inserted_at": r.inserted_at.isoformat() + 'Z',
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


@sites_api.route('/<int:site_id>/reviews', methods=['POST'])
@block_portal_maintenance
@jwt_required()
def create_site_review(site_id):
    """
    Crea una nueva reseña para un sitio histórico específico.
    Requiere autenticación JWT.
    Request Body (JSON):
        "rating": int,      # Puntuación 1-5 (requerido)
        "content": str      # Texto de la reseña, max 1000 chars (requerido)
    """
    try:
        user_id = get_jwt_identity()    # Verificar si anda cuando funciona la autenticación en el frontend

        # Verificar que el sitio existe y es visible
        site = get_visible_historic_site(site_id)
        if not site:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Sitio no encontrado"
                }
            }), 404

        # Validar datos con schema (solo rating y content, site_id viene de la URL)
        review_schema = ReviewCreateSchema()
        try:
            # Agregar site_id del path a los datos
            request_data = request.json or {}
            request_data['historic_site_id'] = site_id
            data = review_schema.load(request_data)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Datos de entrada inválidos",
                    "details": err.messages
                }
            }), 400

        # Crear reseña
        review = create_review_model(
            content=data['content'],
            rating=data['rating'],
            historic_site_id=site_id,
            user_id=user_id
        )

        # Respuesta limpia sin datos sensibles
        return jsonify({
            "id": review.id,
            "site_id": review.historic_site_id,
            "rating": review.rating,
            "content": review.content,
            "user_name": f"{review.user.nombre} {review.user.apellido}",
            "inserted_at": review.inserted_at.isoformat() + 'Z',
            "message": "Reseña creada exitosamente. Será revisada por un moderador."
        }), 201

    except SQLAlchemyError as e:
        error_msg = str(e)
        # Usuario ya reseñó este sitio
        if 'uq_historic_site_and_user' in error_msg or 'UNIQUE constraint' in error_msg:
            return jsonify({
                "error": {
                    "code": "duplicate",
                    "message": "Ya has reseñado este sitio histórico"
                }
            }), 409
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "Error en la base de datos"
            }
        }), 500
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "Ocurrió un error inesperado"
            }
        }), 500


@sites_api.route('/<int:site_id>/reviews/<int:review_id>', methods=['PUT'])
@block_portal_maintenance
@require_feature('reviews_enabled')
@jwt_required()
def update_site_review(site_id, review_id):
    """
    Actualiza una reseña existente de un sitio histórico.
    Solo el autor de la reseña puede actualizarla.
    Requiere autenticación JWT.
    Request Body (JSON):
        "rating": int,      # Puntuación 1-5 (requerido)
        "content": str      # Texto de la reseña (opcional)
    """
    try:
        user_id = get_jwt_identity() # Devuelve un String

        # Verificar que el sitio existe
        site = get_visible_historic_site(site_id)
        if not site:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Sitio no encontrado"
                }
            }), 404

        # Verificar que la reseña existe y pertenece al sitio
        review = get_specific_review(review_id)
        if not review or review.historic_site_id != site_id:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "No se encontró la reseña"
                }
            }), 404

        # Verificar que el usuario es el autor
        if str(review.user_id) != user_id:
            print('forbidden', review.user_id, user_id)
            return jsonify({
                "error": {
                    "code": "forbidden",
                    "message": "Solo puedes actualizar tus propias reseñas"
                }
            }), 403

        # Validar datos con schema
        update_schema = ReviewUpdateSchema()
        try:
            data = update_schema.load(request.json)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Datos de entrada inválidos",
                    "details": err.messages
                }
            }), 400

        # Actualizar reseña
        updated_review = update_data_review(
            review_id,
            rating=data['rating'],
            content=data.get('content')
        )

        if updated_review:
            return jsonify({
                "id": updated_review.id,
                "site_id": updated_review.historic_site_id,
                "rating": updated_review.rating,
                "comment": updated_review.content,
                "user_name": f"{updated_review.user.nombre} {updated_review.user.apellido}",
                "inserted_at": updated_review.inserted_at.isoformat() + 'Z'
            }), 200
        else:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "No se pudo actualizar la reseña"
                }
            }), 404
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "Error inesperado"
            }
        }), 500


@sites_api.route('/<int:site_id>/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
@block_portal_maintenance
@require_feature('reviews_enabled')
def delete_historic_site_review(site_id, review_id):
    """
    Elimina una reseña específica de un sitio histórico.
    Solo el autor de la reseña puede eliminarla.
    Requiere autenticación JWT.
    """
    try:
        user_id = get_jwt_identity()
        
        # Verificar que el sitio existe
        site = get_visible_historic_site(site_id)
        if not site:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Sitio no encontrado"
                }
            }), 404

        # Verificar que la reseña existe y pertenece al sitio
        review = get_specific_review(review_id)
        if not review or review.historic_site_id != site_id:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "No se encontró la reseña"
                }
            }), 404

        # Verificar que el usuario es el autor
        if str(review.user_id) != user_id:
            return jsonify({
                "error": {
                    "code": "forbidden",
                    "message": "Solo puedes eliminar tus propias reseñas"
                }
            }), 403

        # Eliminar la reseña
        if remove_review(review_id):
            return '', 204  # No Content (éxito sin cuerpo de respuesta)
        else:
            return jsonify({
                "error": {
                    "code": "server_error",
                    "message": "No se pudo eliminar la reseña"
                }
            }), 500

    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "Error inesperado"
            }
        }), 500

# =============== Crear sitio =================

@sites_api.route('', methods=['POST'])
@jwt_required()
@block_portal_maintenance
def create_historic_site():
    """
    Crea un nuevo sitio histórico.
    Requiere autenticación JWT.
    
    Usa HistoricSiteCreateSchema para validación automática.
    """
    try:
        # Obtener user_id del JWT token (ya validado por @jwt_required())
        user_id = get_jwt_identity()

        # Validar datos de entrada con schema
        create_schema = HistoricSiteCreateSchema()
        try:
            data = create_schema.load(request.json)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Datos de entrada inválidos",
                    "details": err.messages
                }
            }), 400

        # Los datos ya están validados por el schema
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
            return jsonify({"error": {"code": "invalid_data", "message": "Estado de conservación inválido"}}), 400

        # Obtener categoría por defecto 
        categoria = db.session.query(HistoricSitesCategories).first()
        if not categoria:
            return jsonify({"error": {"code": "server_error", "message": "No hay categorías disponibles"}}), 500

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

        # Formatear respuesta
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
            "thumbnail_url": None,  # Nuevo sitio no tiene thumbnail
            "thumbnail_alt": None
        }

        return jsonify(response_data), 201

    except SQLAlchemyError as e:
        return jsonify({"error": {"code": "server_error", "message": "Error en la base de datos"}}), 500
    except Exception as e:
        return jsonify({"error": {"code": "server_error", "message": "Ocurrió un error inesperado"}}), 500