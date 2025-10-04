from functools import wraps
from flask import session, redirect, url_for, flash
from src.core.models.auth import get_usuario_by_email


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             print("No hay user_id en session")
#             flash("Debes iniciar sesión para acceder a esta página", "warning")
#             return redirect(url_for('auth.login'))
#         return f(*args, **kwargs)
#     return decorated_function


def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar si el usuario está autenticado, puede ser con el decorador acá o en la ruta
            # En la ruta simplifica las pruebas
            user = get_usuario_by_email(session['user'])
            if not user:
                flash("Debes iniciar sesión para acceder a esta página", "warning")
                print("No user found in session")
                return redirect(url_for('auth.login'))
            
            # Utilizar la función has_permission del usuario que maneja toda la lógica
            if not user.has_permission(permission_name):
                flash("No tienes permiso para acceder a esta página", "error")
                return redirect(url_for('home.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def system_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_usuario_by_email(session['user'])
        if not user or not user.system_admin:
            flash("No tienes permiso para acceder a esta página", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
