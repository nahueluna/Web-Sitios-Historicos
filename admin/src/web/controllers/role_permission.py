from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.web.decorator import permission_required

from src.core.models.auth import (
    get_role_by_id,
    assign_permission_to_role,
    remove_permission_from_role,
    get_role_by_name,
    get_permissions_by_role,
    get_all_permissions
)
from src.core.database import db

role_bp = Blueprint('role', __name__, url_prefix='/roles')

@role_bp.route('/', methods=['GET'])
@permission_required('role_index')
def index():
    """Muestra la lista de roles con sus permisos asignados"""
    admin_role = get_role_by_name("admin")
    editor_role = get_role_by_name("editor")
    all_permissions = get_all_permissions()

    print(all_permissions)
    print(admin_role)
    print(editor_role)

    roles_permissions = [
        {
            "id": 0,
            "name": "Todos los Permisos",
            "permissions": [perm.name for perm in all_permissions]
        },
        {
            "id": admin_role.id,
            "name": admin_role.name,
            "permissions": [perm.name for perm in get_permissions_by_role(admin_role)]
        },
        {
            "id": editor_role.id,
            "name": editor_role.name,
            "permissions": [perm.name for perm in get_permissions_by_role(editor_role)]
        },
    ]

    return render_template(
        'role_permission/index.html',
        roles_permissions=roles_permissions
    )


@role_bp.route('/<int:role_id>/add-permission', methods=['POST'])
@permission_required('role_update')
def add_permission(role_id):
    """Agrega un permiso a un rol"""
    role = get_role_by_id(role_id)
    if not role:
        flash("Rol no encontrado", "error")
        return redirect(url_for('role.index'))
    
    # No permitir agregar permisos al rol "user" (usuarios públicos)
    if role.name == 'user':
        flash("No se pueden agregar permisos al rol de Usuario Público", "error")
        return redirect(url_for('role.index'))
    
    permission_name = request.form.get('permission_name')
    if not permission_name:
        flash("Debe seleccionar un permiso", "error")
        return redirect(url_for('role.index'))
    
    try:
        assign_permission_to_role(role, permission_name)
        flash(f"Permiso '{permission_name}' agregado al rol '{role.name}' exitosamente", "success")
    except ValueError as e:
        flash(str(e), "warning")
    except Exception as e:
        flash(f"Error al agregar permiso: {str(e)}", "error")
    
    return redirect(url_for('role.index'))

@role_bp.route('/<int:role_id>/remove-permission', methods=['POST'])
@permission_required('role_update')
def remove_permission(role_id):
    """Remueve un permiso de un rol"""
    role = get_role_by_id(role_id)
    if not role:
        flash("Rol no encontrado", "error")
        return redirect(url_for('role.index'))
    
    # No permitir remover permisos del rol "user" (no debería tener ninguno)
    if role.name == 'user':
        flash("No se pueden remover permisos del rol de Usuario Público", "error")
        return redirect(url_for('role.index'))
    
    permission_name = request.form.get('permission_name')
    if not permission_name:
        flash("Debe especificar un permiso", "error")
        return redirect(url_for('role.index'))
    
    removed = remove_permission_from_role(role, permission_name)
    if removed:
        flash(f"Permiso '{permission_name}' removido del rol '{role.name}' exitosamente", "success")
    else:
        flash(f"El permiso '{permission_name}' no estaba asignado al rol '{role.name}'", "warning")
    
    return redirect(url_for('role.index'))