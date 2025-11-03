import enum
from _datetime import datetime, timezone
from sqlalchemy import String, DateTime, CheckConstraint, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

class ReviewStatus(enum.Enum):
    PENDING = "Pendiente"
    APPROVED = "Aprobada"
    REJECTED = "Rechazada"

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_range"),
        UniqueConstraint("historic_site_id", "user_id", name="uq_historic_site_and_user")
    )

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content : Mapped[str] = mapped_column(String(1000), nullable=False)
    rating : Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ReviewStatus] = mapped_column(Enum(ReviewStatus), nullable=False, default=ReviewStatus.PENDING)
    inserted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    historic_site_id: Mapped[int] = mapped_column(ForeignKey("historic_sites.id"), nullable=False)
    historic_site = relationship("HistoricSites", backref="reviews")
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    user = relationship("Usuario", backref="reviews")
    rejection_reason: Mapped[str] = mapped_column(String(200), nullable=True)


    def json(self):
        return {
            "id": self.id,
            "content": self.content,
            "rating": self.rating,
            "status": {
                "name": self.status.name,
                "value": self.status.value,
            },
            "inserted_at": self.inserted_at.strftime('%d-%m-%Y'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d'),
            "historic_site": {
                "id": self.historic_site_id,
                "name": self.historic_site.site_name,
            },
            "user": {
                "id": self.user.id,
                "email": self.user.email,
            },
            "rejection_reason": self.rejection_reason if self.rejection_reason else None,
        }