from functools import wraps
from flask import session, redirect, url_for, flash
from src.core.models.auth import find_permission_by_name, find_user_by_id


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
            exists_permission = find_permission_by_name(permission_name)
            if not exists_permission:
                print(f"El permiso '{permission_name}' no existe")
                return redirect(url_for('home'))
            user = find_user_by_id(session['user_id'])
            if not user:
                print("Usuario no encontrado en permission_required")
                flash("No tienes permiso para acceder a esta página", "error")
                return redirect(url_for('home'))
            if not user.has_permission(permission_name):
                print(f"Usuario {user.id} con rol {user.role} no tiene permiso {permission_name}")
                flash("No tienes permiso para acceder a esta página", "error")
                return redirect(url_for('home'))
            print(f"Usuario {user.id} con rol {user.role} tiene permiso {permission_name}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def system_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = find_user_by_id(session['user_id'])
        if not user or not user.system_admin:
            print("Usuario no encontrado o no es sys admin")
            flash("No tienes permiso para acceder a esta página", "error")
            return redirect(url_for('home'))
        print(f"Usuario {user.id} es sys admin")
        return f(*args, **kwargs)
    return decorated_function


# def check_maintenance_mode(f):
#     """
#     Decorador que verifica si el sistema está en modo mantenimiento.
#     Si está en modo mantenimiento, redirige a una página de mantenimiento.
#     """
#     @login_required
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#
#     return decorated_function