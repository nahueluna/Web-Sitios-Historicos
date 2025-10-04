#from src.core.models.historic_sites_state.hs_states import HistoricSitesStates
#from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories
#from src.core.models.historic_sites_logs.hs_logs import HistoricSitesLogs
from src.core.database import Base
from src.core.models.search.tags import Tag
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Table, Column
from datetime import datetime, timezone

historic_sites_tags = Table(
    'historic_sites_tags',
    Base.metadata,
    Column('historic_site_id', ForeignKey('historic_sites.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)

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

    tags: Mapped[list["Tag"]] = relationship(secondary=historic_sites_tags)

    # Relaciones
    # Nombre atributo de la clase
    #logs: Mapped["HistoricSitesLogs"] = relationship("HistoricSitesLogs", back_populates="historic_site")
    #category_rel: Mapped["HistoricSitesCategories"] = relationship("HistoricSitesCategories", back_populates="sites")
    #status_rel: Mapped["HistoricSitesStates"] = relationship("HistoricSitesStates", back_populates="sites")


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
            "status": self.status_id,
            "registration_date": (self.registration_date).strftime('%Y-%m-%d'),
            "inauguration_year": (self.inauguration_year).strftime('%Y-%m-%d'),
            "category": self.category_id,
            "visible": self.visible,
        }
