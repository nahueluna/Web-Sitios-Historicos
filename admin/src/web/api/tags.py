from flask import Blueprint, jsonify, request
from src.core.models.search import get_all_tags

tags_api = Blueprint('tags_api', __name__, url_prefix='/api/tags')

@tags_api.route('', methods=['GET'])
def get_tags():
    """
    Obtiene todos los tags disponibles en el sistema.
    
    Retorna:
        200: Lista de todos los tags
        500: Error del servidor
    """
    try:
        tags = get_all_tags()
        data = [t.json() for t in tags]

        return data, 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": {"code": "server_error", "message": "An unexpected error occurred"}}), 500