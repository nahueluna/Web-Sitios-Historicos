from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class HistoricSitesCategories(Base):
    __tablename__ = "historic_sites_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    category: Mapped[str] = mapped_column(nullable=False)

    # Relación inversa
    sites = relationship("HistoricSites", back_populates="category_rel")

    def __init__(self, category: str):
        self.category = category