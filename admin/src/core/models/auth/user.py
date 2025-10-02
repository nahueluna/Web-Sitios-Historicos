from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Boolean, Enum, DateTime, func
from src.core.database import Base
from datetime import datetime, timezone
import enum

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

    def __repr__(self):
        return f'<User - Id: {self.id} - Email: {self.email} - Rol: {self.rol} - Inserted At: {self.inserted_at} - Updated At: {self.updated_at}>'

    def has_permission(self, permission_name: str) -> bool:
        if self.system_admin:
            return True
        elif self.role:
            return self.role.has_permission(permission_name)
        else:
            return False

    def get_name_role(self) -> str:
        if self.system_admin:
            return "System Admin"
        elif self.role:
            return self.role.name
        else:
            return "No Role"
