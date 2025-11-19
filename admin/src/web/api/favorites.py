from flask import Blueprint, jsonify, request, session
from src.core.models.historic_sites import list_historic_sites_with_advanced_filters, get_visible_historic_site
from src.core.models.auth import agregar_favorito, quitar_favorito, get_favoritos, es_favorito
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.review.review import Review, ReviewStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.web.decorator import block_portal_maintenance

favorites_api = Blueprint('favorites_api', __name__, url_prefix='/api/favorites')

# ========================= Favoritos ========================

@favorites_api.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_favorite_sites(user_id):
    """
    Obtiene los favoritos del usuario.
    """
    try:
        #user_id = get_jwt_identity()
        print("User ID for favorites:", user_id)
        sites, msg = get_favoritos(user_id)
        print("Favorites ", sites)
        if sites is None:
            return jsonify({"error": msg}), 404

        return jsonify({
            "favorites": [site.json() for site in sites],
        }), 200

    except Exception as e:
        print("Error al obtener los sitios:", e)
        return jsonify({"error": "Error al obtener los sitios", "details": str(e)}), 500

@favorites_api.route('/<int:site_id>', methods=['POST'])
@block_portal_maintenance
@jwt_required()
def add_favorite(site_id):
    """
    Agrega un sitio a favoritos.
    """
    try:
        user_id = get_jwt_identity()
        usuario, msg = agregar_favorito(user_id, site_id)

        if usuario is None and msg == "Usuario no encontrado":
            return jsonify({"error": msg}), 404

        if usuario is None and msg == "Sitio no encontrado":
            return jsonify({"error": msg}), 404

        # Si ya era favorito → 200 OK igualmente
        return jsonify({"message": msg}), 200

    except Exception as e:
        return jsonify({"error": "Error al agregar favorito", "details": str(e)}), 500

@favorites_api.route('/<int:site_id>', methods=['DELETE'])
@block_portal_maintenance
@jwt_required()
def remove_favorite(site_id):
    """
    Elimina un sitio de favoritos.
    """
    try:
        user_id = get_jwt_identity()
        usuario, msg = quitar_favorito(user_id, site_id)

        if usuario is None and msg == "Usuario no encontrado":
            return jsonify({"error": msg}), 404
        
        if usuario is None and msg == "Sitio no encontrado":
            return jsonify({"error": msg}), 404

        # Si no estaba en favoritos → igual devolver 200 OK
        return jsonify({"message": msg}), 200

    except Exception as e:
        return jsonify({"error": "Error al quitar favorito", "details": str(e)}), 500

@favorites_api.route('/check/<int:site_id>', methods=['GET'])
@block_portal_maintenance
@jwt_required()
def check_favorite(site_id):
    """
    Verifica si un sitio es favorito del usuario.
    Devuelve true/false sin validar existencia.
    """
    try:
        user_id = get_jwt_identity()
        is_fav = es_favorito(user_id, site_id)
        return jsonify({"is_favorite": is_fav}), 200

    except Exception as e:
        return jsonify({"error": "Error al verificar favorito", "details": str(e)}), 500
