from flask import Blueprint, request, jsonify, session, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from src.web.handlers.auth import is_authenticated
from src.core.models.auth import get_usuario_by_email, get_usuario_by_id

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')

@auth_api.post('')
def generate_jwt_token():
    user_email = request.json.get('email')
    if not is_authenticated():
        return jsonify({"error": {
            "code": "invalid_credentials",
            "message": "Credenciales inválidas."
        }}), 401
    
    user = get_usuario_by_email(user_email)
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
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 200

@auth_api.post('/refresh')
@jwt_required(refresh=True)  # Deberia verificar automaticamente el refresh token
def refresh():
    try:
        current_user_id = get_jwt_identity()
        print(f"🔐 Refreshing token for user ID: {current_user_id}")
        
        user = get_usuario_by_id(current_user_id)
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
        
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            "access_token": new_access_token,
        }), 200
        
    except Exception as e:
        print(f"❌ Error in refresh endpoint: {str(e)}")
        return jsonify({"error": {
            "code": "token_invalid",
            "message": "Token de refresh inválido"
        }}), 422

