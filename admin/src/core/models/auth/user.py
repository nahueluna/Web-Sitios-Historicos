from src.core.database import Base, db
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, String, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .role_permission import Role

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    alias: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    system_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=True)

    # Un usuario pertenece a un solo rol (many-to-one)
    # Permite acceder al rol asignado a este usuario
    role: Mapped["Role"] = relationship(back_populates="users")

    inserted_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f'<User - Alias: {self.alias} - Email: {self.email} - Inserted At: {self.inserted_at} - Updated At: {self.updated_at}>'
    
    def assign_role(self, role_name: str) -> bool:
        """
        Asigna un rol específico a este usuario.
        Returns:
            bool: True si la asignación fue exitosa, False en caso contrario
        """
        # No permitir cambiar rol de system admin
        if self.system_admin:
            print(f"No se puede cambiar el rol de un administrador del sistema")
            return False
        
        # Buscar el rol por nombre
        role = db.session.query(Role).filter_by(name=role_name).first()
        if not role:
            print(f"Rol '{role_name}' no encontrado")
            return False
        
        # Verificar si ya tiene el rol asignado
        if self.role_id == role.id:
            print(f"El usuario '{self.alias}' ya tiene el rol '{role_name}' asignado")
            return False
        
        # Asignar el nuevo rol
        old_role_name = self.role.name if self.role else "sin rol"
        self.role_id = role.id
        
        try:
            db.session.commit()
            print(f"Rol '{role_name}' asignado exitosamente al usuario '{self.alias}' (anterior: {old_role_name})")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al asignar rol: {e}")
            return False

    def unassign_role(self) -> bool:
        """
        Desasigna el rol actual de este usuario.
        Returns:
            bool: True si la desasignación fue exitosa, False en caso contrario
        """
        # No permitir desasignar rol de system admin
        if self.system_admin:
            print(f"No se puede desasignar rol de un administrador del sistema")
            return False
        
        # Verificar si tiene rol asignado
        if not self.role_id:
            print(f"El usuario '{self.alias}' no tiene ningún rol asignado")
            return False
        
        # Guardar el rol actual para el mensaje
        current_role_name = self.role.name if self.role else "desconocido"
        
        # Desasignar el rol
        self.role_id = None
        
        try:
            db.session.commit()
            print(f"Rol '{current_role_name}' desasignado exitosamente del usuario '{self.alias}'")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al desasignar rol: {e}")
            return False

    def get_role_name(self) -> str:
        """
        Obtiene el nombre del rol asignado al usuario.
        Returns:
            str: Nombre del rol o información especial para system admin
        """
        if self.system_admin:
            return "system_admin"
        elif self.role:
            return self.role.name
        else:
            return "sin rol"
        
    def has_permission(self, permission_name: str) -> bool:
        """
        Verifica si el usuario tiene un permiso específico.
        Returns:
            bool: True si el usuario tiene el permiso, False en caso contrario
        """
        if self.system_admin:
            return True
        elif self.role:
            return self.role.has_permission(permission_name)
        else:
            return False

    