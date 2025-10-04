from src.core.models.feature_flag.feature_flag import FeatureFlag
from src.core.database import db

def is_enabled(flag_key: str) -> bool:
    """Verifica si un flag está activo"""
    return db.session.query(FeatureFlag).filter_by(name=flag_key, is_enabled=True).first() is not None

def find_flag_by_id(flag_id: int) -> FeatureFlag:
    """Obtiene un flag específico"""
    return db.session.query(FeatureFlag).filter_by(id=flag_id).first()

def get_all_flags():
    """Obtiene todos los flags"""
    return db.session.query(FeatureFlag).all()

def update_flag(flag_id: int, is_enabled: bool, updated_by: int, maintenance_message: str = None, description: str = None):
    """Actualiza un flag específico"""
    flag = db.session.get(FeatureFlag, flag_id)
    if not flag:
        return None
    flag.is_enabled = is_enabled
    flag.updated_by = updated_by
    if maintenance_message is not None:
        flag.maintenance_message = maintenance_message
    if description is not None:
        flag.description = description
    db.session.commit()
    return flag

def initialize_default_flags():
    """Crea los flags por defecto si no existen"""
    default_flags = [
        {
            'name': 'admin_maintenance_mode',
            'maintenance_message': 'El panel de administración está en mantenimiento. Por favor, inténtelo más tarde.',
            'description': 'Bloquea el acceso al panel de administración'
        },
        {
            'name': 'portal_maintenance_mode',
            'description': 'Bloquea el acceso al portal público',
            'maintenance_message': 'El portal público está en mantenimiento. Por favor, inténtelo más tarde.'
        },
        {
            'name': 'reviews_enabled',
            'maintenance_message': 'Las reseñas están deshabilitadas temporalmente.',
            'description': 'Habilita o deshabilita las reseñas en el portal público',
            'is_enabled': True  # Por defecto activo
        }
    ]
    
    for flag_data in default_flags:
        existing = db.session.query(FeatureFlag).filter_by(name=flag_data['name']).first()
        if not existing:
            flag = FeatureFlag(**flag_data)
            db.session.add(flag)
    
    db.session.commit()


