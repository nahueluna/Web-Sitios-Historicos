from flask import Blueprint, render_template
from src.web.decorator import permission_required
from src.core.models.auth.role_permission import Role, Permission, RolePermission
from src.core.database import db

role_bp = Blueprint('role', __name__, url_prefix='/roles')

@role_bp.route('/', methods=['GET'])
@permission_required('role_index')
def index():
    """Muestra la lista de roles con sus permisos asignados"""
    # Obtener todos los roles con sus permisos
    roles = db.session.query(Role).all()
    
    return render_template(
        'role_permission/role_permission.html',
        roles=roles
    )


@role_bp.route('/assign/<int:user_id>', methods=['POST'])
@permission_required('role_assign')
def assign_role(user_id):
    return f"Asignar rol a usuario {user_id}"