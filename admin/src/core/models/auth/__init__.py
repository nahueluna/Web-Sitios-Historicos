from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.models.auth.user import Usuario, RolUsuario
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.auth.role_permission import Role, Permission, RolePermission
from src.core.database import db
from sqlalchemy.exc import IntegrityError
import secrets
import string
import hashlib

class EmailExistente(Exception):
    """Se intento crear un usuario con un email ya registrado"""
    pass

# Utilidades de Contraseña y Autenticación
def generar_password_aleatoria(longitud: int = 8) -> str:
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

# Esta aca en vez de ser metodo de Usuario para evitar circular imports
def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_user(email: str, password: str) -> Usuario | None:
    user = get_usuario_by_email(email)

    # Usuario no existe
    if not user:
        return None

    # Usuario eliminado
    if user.eliminado:
        return None

    # Verificar contraseña
    if not bcrypt.check_password_hash(user.password, password):
        return None

    # Usuario bloqueado (inactivo)
    if not user.activo:
        return None

    # Todo correcto
    return user

# Gestión de Usuarios
def get_all_usuarios():
    return db.session.query(Usuario).filter_by(eliminado=False).all()

def get_usuario_by_id(usuario_id: int):
    return db.session.query(Usuario).filter_by(id=usuario_id, eliminado=False).first()

def get_usuario_by_email(email: str):
    return db.session.query(Usuario).filter_by(email=email, eliminado=False).first()

def crear_usuario(email: str, nombre: str, apellido: str, rol: RolUsuario) -> tuple[Usuario, str]:
    """
    Crea un usuario con contraseña aleatoria.
    Retorna (usuario, password_en_claro).
    """
    password_plano = generar_password_aleatoria()
    password_hash = hash_password(password_plano)

    usuario = Usuario(
        email=email,
        nombre=nombre,
        apellido=apellido,
        password=password_hash,
        rol=rol,
    )

    db.session.add(usuario)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise EmailExistente

    return usuario, password_plano

def actualizar_usuario(
    usuario_id: int,
    email: str = None,
    nombre: str = None,
    apellido: str = None,
    rol: RolUsuario = None,
    activo: bool = None
):
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return None
    
    # No permitir modificar usuarios system_admin
    if usuario.system_admin:
        raise ValueError("No se puede modificar un usuario System Admin")
    
    if email is not None:
        usuario.email = email
    if nombre is not None:
        usuario.nombre = nombre
    if apellido is not None:
        usuario.apellido = apellido
    if rol is not None:
        usuario.rol = rol
    if activo is not None:
        # No permitir desactivar (bloquear) a administradores o system admins
        if not activo and (usuario.rol == RolUsuario.ADMIN or usuario.system_admin):
            raise ValueError("No se puede bloquear a un usuario Administrador")
        usuario.activo = activo

    db.session.commit()
    return usuario

def eliminar_usuario(usuario_id: int):
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return None

    # No permitir eliminar usuarios system_admin
    if usuario.system_admin:
        raise ValueError("No se puede eliminar un usuario System Admin")

    usuario.eliminado = True;
    db.session.commit()
    return usuario

def buscar_usuarios(email=None, activo=None, rol=None, orden="asc", pagina=1, por_pagina=10):
    query = db.session.query(Usuario).filter(~Usuario.eliminado)

    if email:
        query = query.filter(Usuario.email.ilike(f"%{email}%"))
    if activo is not None:
        query = query.filter(Usuario.activo == activo)
    if rol:
        query = query.filter(Usuario.rol == rol)

    if orden == "desc":
        query = query.order_by(Usuario.fecha_creacion.desc())
    else:
        query = query.order_by(Usuario.fecha_creacion.asc())

    total = query.count()
    usuarios = query.offset((pagina - 1) * por_pagina).limit(por_pagina).all()

    return usuarios, total

# Gestión de Roles
def get_role_by_id(role_id: int) -> Role | None:
    """Obtiene un rol por su ID"""
    return db.session.query(Role).filter_by(id=role_id).first()

def get_role_by_name(role_name: str) -> Role | None:
    """Obtiene un rol por su nombre"""
    return db.session.query(Role).filter_by(name=role_name).first()

def get_all_roles() -> list[Role]:
    """Obtiene todos los roles"""
    return db.session.query(Role).all()

def get_permissions_by_role(role: Role) -> list[Permission]:
    """Obtiene todos los permisos asociados a un rol"""
    return [rp.permission for rp in role.role_permissions]


def assign_role(user: Usuario, role_name: str) -> Usuario | None:
        # No permitir cambiar rol de system admin
        if user.system_admin:
            print(f"No se puede cambiar el rol de un administrador del sistema")
            return None

        # Buscar el rol por nombre
        role = db.session.query(Role).filter_by(name=role_name).first()
        if not role:
            print(f"Rol '{role_name}' no encontrado")
            return None

        # Asignar el nuevo rol
        old_role_name = user.role.name if user.role else "sin rol"
        user.role_id = role.id

        db.session.commit()
        print(f"Rol '{role_name}' asignado exitosamente al usuario '{user.name}' (anterior: {old_role_name})")
        return user

# Gestión de Permisos
def get_all_permissions() -> list[Permission]:
    """Obtiene todos los permisos disponibles"""
    return db.session.query(Permission).all()

def create_permission(name: str) -> Permission:
    # Verificar si el permiso ya existe
    existing_permission = db.session.query(Permission).filter_by(name=name).first()
    if existing_permission:
        print(f"El permiso '{name}' ya existe.")
        return existing_permission

    # Crear un nuevo permiso
    new_permission = Permission(name=name)
    db.session.add(new_permission)
    print(f"Permiso '{name}' creado exitosamente.")
    return new_permission

def find_permission_by_name(permission_name: str) -> Permission | None:
    return db.session.query(Permission).filter_by(name=permission_name).first()



# Asignaciones de Permisos a Roles
def assign_permission_to_role(role: Role, permission_name: str):
    """
    Asigna un permiso a un rol.
    Returns:
        RolePermission creado o None si el permiso no existe
    """
    # Buscar el permiso por nombre
    permission = db.session.query(Permission).filter_by(name=permission_name).first()
    if not permission:
        print(f"Permiso '{permission_name}' no encontrado")
        return None

    # Asignar el permiso al rol
    role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
    db.session.add(role_permission)
    db.session.commit()
    print(f"Permiso '{permission_name}' asignado exitosamente al rol '{role.name}'")
    return role_permission

def remove_permission_from_role(role: Role, permission_name: str) -> bool:
    """
    Remueve un permiso de un rol.
    Returns:
        True si se removió exitosamente, 
        False si no existía la asignación, 
        False si el permiso no existe
    """
    # Buscar el permiso por nombre
    permission = db.session.query(Permission).filter_by(name=permission_name).first()
    if not permission:
        return False
    
    # Buscar la asignación
    role_permission = db.session.query(RolePermission).filter_by(
        role_id=role.id,
        permission_id=permission.id
    ).first()
    
    if not role_permission:
        return False
    
    # Remover el permiso del rol
    db.session.delete(role_permission)
    db.session.commit()
    print(f"Permiso '{permission_name}' removido exitosamente del rol '{role.name}'")
    return True

def agregar_favorito(user_id: int, site_id: int):
    """Agrega un sitio a los favoritos del usuario."""
    usuario = db.session.query(Usuario).filter_by(id=user_id, eliminado=False).first()
    if not usuario:
        return None, "Usuario no encontrado"

    sitio = db.session.query(HistoricSites).filter_by(id=site_id, delete=False).first()
    if not sitio:
        return None, "Sitio no encontrado"

    # Si ya es favorito, no duplicar
    if sitio in usuario.favoritos:
        return usuario, "Ya era favorito"

    usuario.favoritos.append(sitio)
    db.session.commit()
    return usuario, "Agregado correctamente"


def quitar_favorito(user_id: int, site_id: int):
    """Quita un sitio de los favoritos del usuario."""
    usuario = db.session.query(Usuario).filter_by(id=user_id, eliminado=False).first()
    if not usuario:
        return None, "Usuario no encontrado"

    sitio = db.session.query(HistoricSites).filter_by(id=site_id, delete=False).first()
    if not sitio:
        return None, "Sitio no encontrado"

    if sitio not in usuario.favoritos:
        return usuario, "No estaba en favoritos"

    usuario.favoritos.remove(sitio)
    db.session.commit()
    return usuario, "Eliminado de favoritos"


def get_favoritos(user_id: int):
    """Obtiene todos los sitios favoritos del usuario."""
    usuario = db.session.query(Usuario).filter_by(id=user_id, eliminado=False).first()
    if not usuario:
        return None, "Usuario no encontrado"

    return usuario.favoritos, "OK"


def es_favorito(user_id: int, site_id: int):
    """Indica si un sitio es favorito del usuario."""
    usuario = db.session.query(Usuario).filter_by(id=user_id, eliminado=False).first()
    if not usuario:
        return False

    return any(s.id == site_id for s in usuario.favoritos)
