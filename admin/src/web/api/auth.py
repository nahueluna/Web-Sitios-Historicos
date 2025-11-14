from flask import Blueprint, request, jsonify, session, current_app
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
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
        return jsonify({"error": {
            "code": "user_not_found",
            "message": "Usuario no existe"
        }}), 401
    
    if not user.activo:
        return jsonify({"error": {
            "code": "user_blocked",
            "message": "Usuario bloqueado"
        }}), 403
    
    # Crear access y refresh tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 200

@auth_api.post('/refresh')
@jwt_required(refresh=True)  # Deberia verificar automaticamente el refresh token
def refresh():
    current_user_id = get_jwt_identity()

    user = get_usuario_by_email(session["user"])
    
    # Usuario eliminano
    if not user:
        return jsonify({"error": {
            "code": "user_not_found", 
            "message": "Usuario no existe"
        }}), 401
    
    # Usuario bloqueado
    if not user.activo:
        return jsonify({"error": {
            "code": "user_blocked",      
            "message": "Usuario bloqueado"
        }}), 403  
    
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        "access_token": new_access_token,
    }), 200