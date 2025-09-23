from src.core.database import db
from src.core.models.auth.user import Usuario, RolUsuario

def get_all_usuarios():
    return db.session.query(Usuario).all()

def get_usuario_by_id(usuario_id: int):
    return db.session.query(Usuario).filter_by(id=usuario_id).first()

def crear_usuario(email: str, nombre: str, apellido: str, password: str, rol: RolUsuario, activo: bool = True):
    usuario = Usuario(
        email=email,
        nombre=nombre,
        apellido=apellido,
        password=password,  # Hash en producción
        rol=rol,
        activo=activo
    )
    db.session.add(usuario)
    db.session.commit()
    return usuario

def actualizar_usuario(usuario_id: int, rol: RolUsuario = None, activo: bool = None):
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        return None
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
