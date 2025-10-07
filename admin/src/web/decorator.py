from functools import wraps
from flask import session, redirect, url_for, flash, abort, render_template
from src.core.models.auth import get_usuario_by_email
from src.core.models.feature_flag import is_active, find_flag_by_name


# DECORADORES DE PERMISOS

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
        if not user.is_system_admin():
            flash("No tienes permisos para acceder a esta página. Solo administradores del sistema.", "error")
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function




# DECORADORES DE FEATURE FLAGS

def require_feature(flag_name: str):
    """
    Requiere que un feature flag esté habilitado para acceder a la ruta.
    
    Uso: Funcionalidades opcionales del sistema
    - reviews_enabled
    - export_csv_enabled
    - new_search_algorithm
    
    Comportamiento:
    - Si flag está OFF → Bloquea acceso (403)
    - Si flag está ON → Permite acceso
    - System admins siempre tienen acceso
    
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            
            user = get_usuario_by_email(session.get('user'))
            
            # System admins siempre tienen acceso
            if user and user.system_admin:
                return f(*args, **kwargs)
            
            # Verificar si el feature no está habilitado
            if not is_active(flag_name):
                
                flag = find_flag_by_name(flag_name)
                
                return render_template(
                    'maintenance.html',
                    maintenance_message=flag.maintenance_message
                ), 403  # 403 Forbidden: La funcionalidad existe pero está deshabilitada (feature flag OFF)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def block_admin_maintenance(f):
    """
    Bloquea el acceso al panel de administración cuando está en modo mantenimiento.
    
    Flag verificado: 'admin_maintenance_mode'
    
    Comportamiento:
    - Si admin_maintenance_mode está ON → Bloquea acceso (503)
    - Si admin_maintenance_mode está OFF → Permite acceso
    - System Admins SIEMPRE pueden acceder (incluso con mantenimiento ON)
    - Administradores y Editores SON bloqueados durante mantenimiento
    
    Muestra mensaje de mantenimiento personalizado configurado en el flag.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Verificar si el modo mantenimiento de admin está ACTIVO (ON)
        if is_active('admin_maintenance_mode'):
            # Sistema en mantenimiento
            
            # Verificar si el usuario es System Admin (pueden acceder siempre)
            user = get_usuario_by_email(session.get('user'))

            if user and user.is_system_admin():
                # System Admin puede acceder durante mantenimiento
                return f(*args, **kwargs)

            # Obtener el flag para mostrar el mensaje personalizado
            flag = find_flag_by_name('admin_maintenance_mode')
            
            # Renderizar template de mantenimiento
            return render_template(
                'maintenance.html',
                maintenance_message=flag.maintenance_message
            ), 503  # 503 Service Unavailable: El servicio está temporalmente en mantenimiento
        
        
        # No se bloquean funcionalidades de admin y editor → Permitir acceso
        return f(*args, **kwargs)
    
    return decorated_function


def block_portal_maintenance(f):
    """
    Bloquea el acceso al portal público cuando está en modo mantenimiento.
    
    Flag verificado: 'portal_maintenance_mode'
    
    Comportamiento:
    - Si portal_maintenance_mode está ON → Bloquea acceso (503)
    - Si portal_maintenance_mode está OFF → Permite acceso
    - System Admins y roles exentos pueden acceder durante mantenimiento
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):

        
        # Verificar si el modo mantenimiento de portal está ACTIVO (ON)
        if is_active('portal_maintenance_mode'):
            # Portal en mantenimiento

            user = get_usuario_by_email(session.get('user'))
            if user and user.system_admin:
                # System Admin puede acceder durante mantenimiento
                return f(*args, **kwargs)
            
            
            # Usuario NO tiene rol exento → Bloquear acceso
            
            # Obtener mensaje personalizado del flag
            flag = find_flag_by_name('portal_maintenance_mode')

            # Renderizar template de mantenimiento
            return render_template(
                'maintenance.html',
                maintenance_message=flag.maintenance_message
            ), 503  # 503 Service Unavailable: El servicio está temporalmente en mantenimiento
        
        
        # Portal operando normalmente → Permitir acceso
        return f(*args, **kwargs)
    
    return decorated_function