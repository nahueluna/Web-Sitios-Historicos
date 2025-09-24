from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime, timezone

class HistoricSitesLogs(Base):
    __tablename__ = "historic_sites_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    log_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    historic_site_id: Mapped[int] = mapped_column(ForeignKey("historic_sites.id"), nullable=False)
    #user_id: Mapped[id] = mapped_column(ForeignKey("users.id"))
    action_type: Mapped[str] = mapped_column(ForeignKey("log_actions.id"), nullable=False)

    # Relaciones
    historic_site: Mapped[HistoricSites] = relationship("HistoricSites", back_populates="logs")
    #user: Mapped["User"] = relationship("User", back_populates="site_logs")

    def __init__(self, historic_site_id: int, action_type_id: int):
        self.historic_site_id = historic_site_id
        self.action_type = action_type_id