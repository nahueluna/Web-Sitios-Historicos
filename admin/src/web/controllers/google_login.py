from src.core.models.auth.user import RolUsuario
from flask import Blueprint, request, session, jsonify
from src.core.models.auth import crear_usuario, get_usuario_by_email
from flask_jwt_extended import jwt_required, get_jwt_identity

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

bp_google_auth = Blueprint("google", __name__, url_prefix="/google")

@bp_google_auth.post("/auth")
def register_login():
    try:
        token = request.json.get("credential")
        if not token:
            return jsonify({"status": "error", "message": "Token de Google no recibido"}), 400

        # Verificar el token
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
        email = idinfo["email"]
        nombre = idinfo.get("given_name")
        apellido = idinfo.get("family_name")
        picture = idinfo.get("picture")


        # Buscar usuario
        user = get_usuario_by_email(email)
        if not user:
            user = crear_usuario(email=email, nombre=nombre, apellido=apellido, rol=RolUsuario.PUBLICO)
        
        elif not user.activo:
            return jsonify({"status": "error", "message": "Cuenta bloqueada"}), 403

        session["user"] = email

        response = {
            "status": "success",
            "message": "Inicio de sesión correcto con Google.",
            "user": {"email": email, "name": nombre, "lastname": apellido, "picture": picture, "id": str(user.id)}
        }
        return jsonify(response), 200

    except ValueError:
        return jsonify({"status": "error", "message": "Token de Google inválido"}), 401
    

@bp_google_auth.post("/logout")
@jwt_required()
def logout():
    if session.get("user"):
        print("Se cerró sesión de:", session.get("user"))
        session.pop("user")
        return jsonify({"status": "success", "message": "Has cerrado sesión correctamente."}), 200
    else:
        return jsonify({"status": "error", "message": "No has iniciado sesión."}), 400