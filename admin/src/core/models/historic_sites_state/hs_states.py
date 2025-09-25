from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class HistoricSitesStates(Base):
    __tablename__ = "historic_sites_states"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, )

    state: Mapped[str] = mapped_column(nullable=False)

    # Relación inversa
    sites = relationship("HistoricSites", back_populates="status_rel")

    def __repr__(self): return f"{self.state}"

    def __init__(self, state: str):
        self.state = state