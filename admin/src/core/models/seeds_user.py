from src.core.models.auth.user import Usuario as User
from src.core.models.auth.role_permission import Role, Permission, RolePermission
from src.core.database import db
from src.core.models.auth import create_permission, assign_permission_to_role


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
    permission_user_index = create_permission("user_index")
    permission_user_new = create_permission("user_new")
    permission_user_update = create_permission("user_update")
    permission_user_destroy = create_permission("user_destroy")
    permission_user_show = create_permission("user_show")
    
    # Permisos para sitios históricos
    permission_site_index = create_permission("site_index")
    permission_site_new = create_permission("site_new")
    permission_site_update = create_permission("site_update")
    permission_site_destroy = create_permission("site_destroy")
    permission_site_show = create_permission("site_show")

    # Permisos para moderación de reseñas
    permission_review_index = create_permission("review_index")
    permission_review_moderate = create_permission("review_moderate")
    permission_review_destroy = create_permission("review_destroy")

    # Permisos para gestión de roles
    permission_role_assign = create_permission("role_assign")
    permission_role_index = create_permission("role_index")
    permission_role_update = create_permission("role_update")
    

    print("Permisos de prueba creados.")

    print("Asignando permisos a roles...")
    
    # Permisos para EDITOR (administrar sitios históricos y validar)
    editor_permission_names = [
        "site_index", "site_new", "site_update", "site_destroy", "site_show",
        "review_index", "review_moderate", "review_destroy"
    ]
    
    for perm_name in editor_permission_names:
        assign_permission_to_role(role_editor, perm_name)
    
    # Permisos para ADMIN (todo lo del editor + gestión de usuarios)
    admin_permission_names = editor_permission_names + [
        "user_index", "user_new", "user_update", "user_destroy", "user_show",
        "role_assign", "role_index", "role_update"
    ]
    
    for perm_name in admin_permission_names:
        assign_permission_to_role(role_admin, perm_name)
    
    print("Permisos asignados a roles.")

    print("Creación de usuarios")
    # System admin con acceso completo (sin rol específico con system_admin=True)
    sys_admin = User(
        email="sys_admin@example.com", 
        nombre="System",
        apellido="Admin",
        alias="sys_admin",
        password="sys_admin123",
        system_admin=True,  
        enabled=True,
        role_id=None  # System admin no necesita rol específico
    )
    
    # Administrador (asignado al rol admin)
    admin = User(
        email="admin@example.com", 
        nombre="Admin",
        apellido="User",
        alias="admin", 
        password="admin123",
        role_id=role_admin.id,
        enabled=True
    )
    
    # Editor (asignado al rol editor)
    editor = User(
        email="editor@example.com", 
        nombre="Editor",
        apellido="User",
        alias="editor", 
        password="editor123",
        role_id=role_editor.id,
        enabled=True
    )
    
    # Usuario público (asignado al rol user)
    user = User(
        email="user@example.com", 
        nombre="Public",
        apellido="User",
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

