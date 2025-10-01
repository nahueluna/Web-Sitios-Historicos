from src.core.database import db
from src.core.models.auth.user import Usuario, RolUsuario
from src.core.models.auth.role_permission import Role, Permission, RolePermission
from src.core.database import db
from sqlalchemy.exc import IntegrityError
import secrets
import string
import hashlib

class EmailExistente(Exception):
    """Se intento crear un usuario con un email ya registrado"""
    pass

def generar_password_aleatoria(longitud: int = 8) -> str:
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_all_usuarios():
    return db.session.query(Usuario).all()

def get_usuario_by_id(usuario_id: int):
    return db.session.query(Usuario).filter_by(id=usuario_id).first()


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
        rol=rol
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
    if email is not None:
        usuario.email = email
    if nombre is not None:
        usuario.nombre = nombre
    if apellido is not None:
        usuario.apellido = apellido
    if rol is not None:
        usuario.rol = rol
    if activo is not None:
        usuario.activo = activo

    db.session.commit()
    return usuario

def eliminar_usuario(usuario_id: int):
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return None
    db.session.delete(usuario)
    db.session.commit()
    return usuario

def buscar_usuarios(email=None, activo=None, rol=None, orden="asc", pagina=1, por_pagina=10):
    query = db.session.query(Usuario)

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


# Ver si se puede reemplazar por el método de arriba get_user_by_id o viceversa
def find_user_by_id(user_id: int) -> Usuario | None:
        return db.session.query(Usuario).filter_by(id=user_id).first()


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


def assign_permission_to_role(role: Role, permission_name: str):
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
        
def find_permission_by_name(permission_name: str) -> Permission | None:
    return db.session.query(Permission).filter_by(name=permission_name).first()
