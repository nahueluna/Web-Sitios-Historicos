from flask import Blueprint, render_template
from src.web.decorator import login_required, permission_required, system_admin_required

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
@login_required
@permission_required('user_index')
def index():
    return render_template('gestion_usuarios.html')

@user_bp.route('/new', methods=['GET'])
@login_required
@permission_required('user_new')
def new():
    return "Formulario para crear usuario"

@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
@permission_required('user_show')
def show(user_id):
    return f"Detalle del usuario {user_id}"

@user_bp.route('/<int:user_id>/edit', methods=['GET'])
@login_required
@permission_required('user_update')
def edit(user_id):
    return f"Formulario para editar usuario {user_id}"

@user_bp.route('/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_enabled(user_id):
    return f"Toggle enabled para usuario {user_id}"


