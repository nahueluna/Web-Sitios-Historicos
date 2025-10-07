
from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime, timezone

class HistoricSites(Base):
    __tablename__ = "historic_sites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    site_name: Mapped[str] = mapped_column(nullable=False)

    short_description: Mapped[str] = mapped_column(nullable=False)
    long_description: Mapped[str] = mapped_column(nullable=False)

    city: Mapped[str] = mapped_column(nullable=False)
    province: Mapped[str] = mapped_column(nullable=False)

    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    registration_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    inauguration_year: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    visible: Mapped[bool] = mapped_column(nullable=False, default=True)

    status_id: Mapped[int] = mapped_column(ForeignKey("historic_sites_states.id"), nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("historic_sites_categories.id"), nullable=False)

    delete: Mapped[bool] = mapped_column(nullable=False, default=False)

    # Relacion con tabla de tags
    tags = relationship("Tag", secondary="historic_sites_tags", back_populates="historic_sites")

    # Relacion con tabla de estados
    status = relationship("HistoricSitesStates", back_populates="historic_sites")


    def json(self):
        return {
            "id": self.id,
            "site_name": self.site_name,
            "short_description": self.short_description,
            "long_description": self.long_description,
            "city": self.city,
            "province": self.province,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "inauguration_year": (self.inauguration_year).strftime('%Y-%m-%d'),
            "registration_date": self.registration_date.strftime('%d-%m-%Y'),
            "category": self.category_id,
            "visible": self.visible,
            "tags": [tag.name for tag in self.tags],
            "status": self.status.state,
            "status_id": self.status_id
        }
