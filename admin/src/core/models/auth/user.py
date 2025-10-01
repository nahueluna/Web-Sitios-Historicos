from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum, DateTime, func
from src.core.database import Base
from datetime import datetime
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
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<Usuario {self.email} ({self.rol.value})>"
