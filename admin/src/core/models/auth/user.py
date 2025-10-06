from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, Enum, DateTime, func
from src.core.database import Base
from datetime import datetime, timezone
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from src.core.models.auth.role_permission import Role


# Enumeración para los roles de usuario
class RolUsuario(enum.Enum):
    PUBLICO = "Usuario público"
    EDITOR = "Editor"
    ADMIN = "Administrador"

# Modelo Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # guardar hash, no plano
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario), default=RolUsuario.PUBLICO, nullable=False)
    # Reemplazar por inserted_at
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=True)
    system_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ultima_modificacion: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relación con Role
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    def __repr__(self):
        return f'<User - Id: {self.id} - Email: {self.email} - Rol: {self.rol} - Inserted At: {self.inserted_at} - Updated At: {self.updated_at}>'

    def has_permission(self, permission_name: str) -> bool:
        # Los System Admins tienen todos los permisos
        if self.system_admin:
            print(f"User {self.nombre} is a system admin and has all permissions.")
            return True
        
        # Si no tiene rol asignado, no tiene permisos
        if not self.role_id or not self.role:
            print(f"User {self.id} has no role assigned")
            return False
        
        # Verificar si el rol tiene el permiso
        if self.role.has_permission(permission_name):
            print(f"User {self.nombre} with role {self.role.nombre} has permission: {permission_name}")
            return True
            
        return False

    def get_name_role(self) -> str:
        if self.system_admin:
            return "System Admin"
        elif self.role:
            return self.role.name
        else:
            return "No Role"
        
    def is_system_admin(self) -> bool:
        return self.system_admin

    def __repr__(self):
        return f'<User Email: {self.email} - Rol: {self.rol} - Fecha de Creación: {self.fecha_creacion} - Fecha de Actualización: {self.ultima_modificacion}>'