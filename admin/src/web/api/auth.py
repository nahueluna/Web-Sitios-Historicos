from flask import Blueprint, request, jsonify, session, current_app
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from src.web.handlers.auth import is_authenticated
from src.core.models.auth import get_usuario_by_email

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')

@auth_api.post('')
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
