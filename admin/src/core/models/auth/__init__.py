
from src.core.models.auth.user import User
from src.core.models.auth.role_permission import Role, Permission, RolePermission
from src.core.database import db

def find_user_by_id(user_id: int) -> User | None:
        return db.session.query(User).filter_by(id=user_id).first()


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

def assign_role(user: User, role_name: str) -> User | None:
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
        
