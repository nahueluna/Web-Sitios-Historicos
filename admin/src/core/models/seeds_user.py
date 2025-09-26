from src.core.models.auth.user import User
from src.core.models.auth.role_permission import Role, Permission, RolePermission
from src.core.database import db


def run_seeds():
    print("Creación de roles")
    role_user = Role(name="user")
    role_editor = Role(name="editor")
    role_admin = Role(name="admin")
    
    db.session.add(role_user)
    db.session.add(role_editor)
    db.session.add(role_admin)
    db.session.flush()  # Para obtener los IDs
    print("Roles de prueba creados.")

    print("Creación de permisos")
    # Permisos para gestión de usuarios
    permission_user_index = Permission(name="user_index", description="Listar usuarios")
    permission_user_new = Permission(name="user_new", description="Crear usuario")
    permission_user_update = Permission(name="user_update", description="Actualizar usuario")
    permission_user_destroy = Permission(name="user_destroy", description="Eliminar usuario")
    permission_user_show = Permission(name="user_show", description="Ver detalle de usuario")
    
    # Permisos para sitios históricos
    permission_site_index = Permission(name="site_index", description="Listar sitios históricos")
    permission_site_new = Permission(name="site_new", description="Crear sitio histórico")
    permission_site_update = Permission(name="site_update", description="Actualizar sitio histórico")
    permission_site_destroy = Permission(name="site_destroy", description="Eliminar sitio histórico")
    permission_site_show = Permission(name="site_show", description="Ver detalle de sitio histórico")

    # Permisos para moderación de reseñas
    permission_review_index = Permission(name="review_index", description="Listar reseñas")
    permission_review_moderate = Permission(name="review_moderate", description="Moderar reseñas")
    permission_review_destroy = Permission(name="review_destroy", description="Eliminar reseñas")

    permissions = [
        permission_user_index, permission_user_new, permission_user_update, 
        permission_user_destroy, permission_user_show,
        permission_site_index, permission_site_new, permission_site_update, 
        permission_site_destroy, permission_site_show,
        permission_review_index, permission_review_moderate, permission_review_destroy
    ]
    
    for permission in permissions:
        db.session.add(permission)
    db.session.flush()
    print("Permisos de prueba creados.")

    print("Asignando permisos a roles...")
    
    # Permisos para EDITOR (administrar sitios históricos y validar)
    editor_permissions = [
        permission_site_index, permission_site_new, permission_site_update, 
        permission_site_destroy, permission_site_show,
        permission_review_index, permission_review_moderate, permission_review_destroy
    ]
    
    for permission in editor_permissions:
        role_permission = RolePermission(role_id=role_editor.id, permission_id=permission.id)
        db.session.add(role_permission)
    
    # Permisos para ADMIN (todo lo del editor + gestión de usuarios)
    admin_permissions = editor_permissions + [
        permission_user_index, permission_user_new, permission_user_update, 
        permission_user_destroy, permission_user_show
    ]
    
    for permission in admin_permissions:
        role_permission = RolePermission(role_id=role_admin.id, permission_id=permission.id)
        db.session.add(role_permission)
    
    print("Permisos asignados a roles.")

    print("Creación de usuarios")
    # System admin con acceso completo (sin rol específico con system_admin=True)
    sys_admin = User(
        email="sys_admin@example.com", 
        alias="sys_admin", 
        password="sys_admin123",
        system_admin=True,  
        enabled=True,
        role_id=None  # System admin no necesita rol específico
    )
    
    # Administrador (asignado al rol admin)
    admin = User(
        email="admin@example.com", 
        alias="admin", 
        password="admin123",
        role_id=role_admin.id,
        enabled=True
    )
    
    # Editor (asignado al rol editor)
    editor = User(
        email="editor@example.com", 
        alias="editor", 
        password="editor123",
        role_id=role_editor.id,
        enabled=True
    )
    
    # Usuario público (asignado al rol user)
    user = User(
        email="user@example.com", 
        alias="user", 
        password="user123",
        role_id=role_user.id,
        enabled=True
    )
    
    # Guardar usuarios
    db.session.add(sys_admin)
    db.session.add(admin)
    db.session.add(editor)
    db.session.add(user)
    
    db.session.commit()
    
    print("Usuarios de prueba creados con roles asignados:")
    print(f"- System Admin: {sys_admin.alias} (system_admin=True)")
    print(f"- Administrador: {admin.alias} (rol: {role_admin.name})")
    print(f"- Editor: {editor.alias} (rol: {role_editor.name})")
    print(f"- Usuario público: {user.alias} (rol: {role_user.name})")
    print("Seeds ejecutados exitosamente.")

