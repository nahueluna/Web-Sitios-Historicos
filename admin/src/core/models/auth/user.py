from src.core.database import Base
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