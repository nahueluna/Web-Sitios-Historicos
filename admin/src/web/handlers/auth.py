from functools import wraps
from flask import session, redirect, url_for, flash, abort
from src.core.models.auth import RolUsuario, get_usuario_by_email

def is_authenticated():
    return session.get("user") is not None

def is_system_admin():
    """Verifica si el usuario autenticado es un administrador del sistema"""
    if not is_authenticated():
        return False
    user = get_usuario_by_email(session.get("user"))
    return user and user.system_admin

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash("Debes iniciar sesión para acceder a esta página", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles: list[RolUsuario]):
    """Verifica que el usuario este logueado, tenga uno de los roles necesarios y pasa el usuario a la funcion decorada."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Verificar login
            user_email = session.get("user")
            if not user_email:
                flash("Debes iniciar sesión para acceder a esta página", "warning")
                return redirect(url_for("auth.login"))
            

            # 2. Obtener el usuario
            user = get_usuario_by_email(user_email)
            if user.system_admin:
                return f(user, *args, **kwargs)

            if not user:
                abort(500)

            # 3. Verificar rol
            if user.rol not in roles:
                abort(403)

            # 4. Pasar usuario a la vista
            return f(user, *args, **kwargs)
        return decorated_function
    return decorator
