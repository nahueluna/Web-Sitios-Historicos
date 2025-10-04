from flask import Blueprint, session, jsonify, render_template, request
from src.core.models.feature_flag.feature_flag import FeatureFlag
from src.core.database import db
from src.core.models.auth.user import Usuario
from src.core.models.auth import get_usuario_by_email
from src.core.models.feature_flag import get_all_flags, find_flag_by_id
from src.web.decorator import system_admin_required
from src.web.handlers.auth import login_required

feature_flag_bp = Blueprint('feature_flag', __name__, url_prefix='/feature_flags')

@feature_flag_bp.route('/', methods=['GET'])
@login_required
@system_admin_required
def get_feature_flags():
    """Obtiene todos los feature flags"""
    flags = get_all_flags()
    flags_data = []
    for flag in flags:
        # Formatear fechas para mejor legibilidad
        inserted_at_formatted = flag.inserted_at.strftime('%Y-%m-%d %H:%M') if flag.inserted_at else ''
        updated_at_formatted = flag.updated_at.strftime('%Y-%m-%d %H:%M') if flag.updated_at else ''
        
        flags_data.append({
            'id': flag.id,
            'name': flag.name,
            'is_enabled': flag.is_enabled,
            'description': flag.description,
            'maintenance_message': flag.maintenance_message,
            'inserted_at': inserted_at_formatted,
            'updated_at': updated_at_formatted,
            'updated_by': flag.updated_by
        })
    return render_template('feature_flags/index.html', flags=flags_data)


@feature_flag_bp.route('/<int:flag_id>', methods=['POST'])
@login_required
@system_admin_required
def update_feature_flag(flag_id: int):
    """Actualiza un feature flag (e.g., mensaje de mantenimiento)"""
    data = request.json
    
    maintenance_message = data.get('maintenance_message')
    description = data.get('description')

    # Validación del mensaje de mantenimiento
    if maintenance_message is None:
        return jsonify({'error': 'El mensaje de mantenimiento es obligatorio.'}), 400
    if len(maintenance_message) > 255:
        return jsonify({'error': 'El mensaje de mantenimiento no puede exceder 255 caracteres.'}), 400

    flag = db.session.get(FeatureFlag, flag_id)
    if not flag:
        return jsonify({'error': 'Flag no encontrado'}), 404

    # Actualizar los campos del flag
    flag.maintenance_message = maintenance_message
    if description is None:
        flag.description = ""
    else:
        flag.description = description

    user = get_usuario_by_email(session.get('user'))
    flag.updated_by = user.id
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Feature flag actualizado correctamente'})


@feature_flag_bp.route('/<int:flag_id>/toggle', methods=['POST'])
@login_required
@system_admin_required
def toggle_feature_flag(flag_id: int):
    """Activa o desactiva un feature flag"""
    flag = find_flag_by_id(flag_id)

    if not flag:
        return jsonify({'error': 'Flag no encontrado'}), 404

    flag.is_enabled = not flag.is_enabled
    user = get_usuario_by_email(session.get('user'))
    flag.updated_by = user.id
    db.session.commit()
    return jsonify({'id': flag.id, 'is_enabled': flag.is_enabled})