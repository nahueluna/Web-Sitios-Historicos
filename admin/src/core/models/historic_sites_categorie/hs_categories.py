from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class HistoricSitesCategories(Base):
    __tablename__ = "historic_sites_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    category: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"{self.category}"