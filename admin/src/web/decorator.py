from functools import wraps
from flask import session, redirect, url_for, flash, abort
from src.core.models.auth import get_usuario_by_email

def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obtengo el usuario autenticado
            user = get_usuario_by_email(session['user'])
            
            # Utilizar la función has_permission del usuario que maneja toda la lógica
            if not user.has_permission(permission_name):
                flash("No tienes permiso para acceder a esta página", "error")
                return redirect(url_for('home.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def system_admin_required(f):
    """Decorador que verifica que el usuario esté autenticado y sea un administrador del sistema (sys_admin)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Obtener el usuario autenticado desde la sesión
        user_email = session.get('user')

        # 2. Obtener el usuario desde la base de datos
        user = get_usuario_by_email(user_email)
        if not user:
            flash("Usuario no encontrado. Por favor, inicia sesión nuevamente.", "error")
            return redirect(url_for('auth.login'))
        
        # 3. Verificar que sea un administrador del sistema
        # El método de arriba cumple la misma función con has_permission del usuario
        # Por claridad utilizo éste
        if not user.system_admin:
            flash("No tienes permisos para acceder a esta página. Solo administradores del sistema.", "error")
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function
