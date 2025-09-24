from src.core.models.historic_sites_state.hs_states import HistoricSitesStates
from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories
from src.core.models.historic_sites_logs.hs_logs import HistoricSitesLogs
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

    # Relaciones
    # Nombre atributo de la clase
    logs: Mapped["HistoricSitesLogs"] = relationship("HistoricSitesLogs", back_populates="logs")
    category_rel: Mapped["HistoricSitesCategories"] = relationship("HistoricSitesCategories", back_populates="sites")
    status_rel: Mapped["HistoricSitesStates"] = relationship("HistoricSitesStates", back_populates="sites")


    def init__(
            self, site_name: str, short_description: str, long_description: str, city: str, 
            province: str, latitude: float, longitude: float, conservation_status: str, 
            inauguration_year: datetime, category: str, visible: bool = True
        ):
        self.site_name = site_name
        self.short_description = short_description
        self.long_description = long_description
        self.city = city
        self.province = province
        self.latitude = latitude
        self.longitude = longitude
        self.status_id = conservation_status
        self.inauguration_year = inauguration_year
        self.category_id = category
        self.visible = visible
