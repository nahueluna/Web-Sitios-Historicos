from flask import Blueprint, render_template, request

# Modelos
from src.core.models.auth.user import RolUsuario
# Handlers y decoradores
from src.web.decorator import block_admin_maintenance
from src.web.handlers.auth import role_required

advanced_search_bp = Blueprint('advanced_search', __name__, url_prefix='/buscar')


@advanced_search_bp.get('/')
@block_admin_maintenance
def advanced_search():
    # LA BUSQUEDA DEPENDE DE LAS CONSULTAS A LA BASE DE DATOS
    return render_template('advanced_search/index.html')

