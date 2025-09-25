from src.core.model.auth.user import User
from src.core.model.auth.roles_permissions import Role, Permission


def run_seeds():
    print("Creando usuarios de prueba...")
    sys_admin = User(email="sys_admin@example.com", alias="sys_admin", password="sys_admin123")
    admin = User(email="admin@example.com", alias="admin", password="admin123")
    editor = User(email="editor@example.com", alias="editor", password="editor123")
    user = User(email="user@example.com", alias="user", password="user123")
    print("Usuarios de prueba creados.")

    print("Creando roles de prueba...")
    role_sys_admin = Role(name="sys_admin", description="Administrador del sistema")
    role_admin = Role(name="admin", description="Administrador del sistema")
    role_editor = Role(name="editor", description="Editor de contenido")
    role_user = Role(name="user", description="Usuario estándar")
    print("Roles de prueba creados.")

    print("Creando permisos de prueba...")
    permission_sys_admin = Permission(name="sys_admin", description="Permiso para administrar el sistema")
    permission_create = Permission(name="create_user", description="Permiso para crear contenido")
    permission_edit = Permission(name="edit_content", description="Permiso para editar contenido")
    permission_delete = Permission(name="delete_content", description="Permiso para eliminar contenido")
    print("Permisos de prueba creados.")

