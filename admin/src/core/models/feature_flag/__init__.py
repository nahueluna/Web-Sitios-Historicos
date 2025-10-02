# services/feature_flag_service.py
from src.core.database import db
from src.core.models.feature_flag import FeatureFlag

class FeatureFlagService:
    
    @staticmethod
    def is_enabled(flag_key: str) -> bool:
        """Verifica si un flag está activo"""
        return db.session.query(FeatureFlag).filter_by(name=flag_key, is_enabled=True).first() is not None

    @staticmethod
    def get_flag(flag_key: str):
        """Obtiene un flag específico"""
        return db.session.query(FeatureFlag).filter_by(name=flag_key).first()

    @staticmethod
    def get_all_flags():
        """Obtiene todos los flags"""
        return db.session.query(FeatureFlag).all()

    @staticmethod
    def get_flag(flag_key: str):
        """Obtiene un flag específico"""
        return db.session.query(FeatureFlag).filter_by(name=flag_key).first()
    
    
    @staticmethod
    def set_flag(name: str, is_enabled: bool, updated_by: int, maintenance_message: str = None):
        """Actualiza el estado de un flag"""
        flag = db.session.query(FeatureFlag).filter_by(name=name).first()
        if flag:
            flag.is_enabled = is_enabled
            flag.updated_by = updated_by
            if maintenance_message is not None:
                flag.maintenance_message = maintenance_message
            db.session.commit()
        return flag
    
    @staticmethod
    def initialize_default_flags():
        """Crea los flags por defecto si no existen"""
        default_flags = [
            {
                'name': 'admin_maintenance_mode',
                'description': 'Bloquea el acceso al panel de administración',
                'maintenance_message': 'El panel de administración está en mantenimiento. Por favor, inténtelo más tarde.'
            },
            {
                'name': 'portal_maintenance_mode',
                'description': 'Bloquea el acceso al portal público',
                'maintenance_message': 'El portal público está en mantenimiento. Por favor, inténtelo más tarde.'
            },
            {
                'name': 'reviews_enabled',
                'description': 'Habilita la creación de reseñas en el portal',
                'is_enabled': True  # Por defecto activo
            }
        ]
        
        for flag_data in default_flags:
            existing = FeatureFlag.query.filter_by(key=flag_data['key']).first()
            if not existing:
                flag = FeatureFlag(**flag_data)
                db.session.add(flag)
        
        db.session.commit()


