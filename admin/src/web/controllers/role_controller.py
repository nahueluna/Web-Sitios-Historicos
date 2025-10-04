from flask import Blueprint
from src.web.decorator import permission_required

role_bp = Blueprint('role', __name__, url_prefix='/roles')

@role_bp.route('/', methods=['GET'])
@permission_required('role_index')
def index():
    return "Lista de roles"


@role_bp.route('/assign/<int:user_id>', methods=['POST'])
@permission_required('role_assign')
def assign_role(user_id):
    return f"Asignar rol a usuario {user_id}"