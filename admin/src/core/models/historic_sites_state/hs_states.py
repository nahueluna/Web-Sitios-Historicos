from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class HistoricSitesStates(Base):
    __tablename__ = "historic_sites_states"

    state: Mapped[str] = mapped_column(nullable=False, primary_key=True)

    def __repr__(self) -> str:
        return f"{self.state}"