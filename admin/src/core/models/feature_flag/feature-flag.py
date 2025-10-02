from src.core.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, String, Boolean, Integer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.models.auth.user import User

class FeatureFlag(Base):
    __tablename__ = 'feature_flags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Unique name for the feature flag: 
    # admin_maintenance_mode, portal_maintenance_mode and reviews_enabled
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    maintenance_message: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    
    inserted_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    updated_by: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)

    # Relación con el usuario que actualizó (sysAdmin)
    updated_by_user: Mapped["User"] = relationship("User")