from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class HistoricSitesTags(Base):
    __tablename__ = "historic_sites_tags"

    site_id: Mapped[int] = mapped_column(ForeignKey('historic_sites.id'), nullable=False, primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), nullable=False, primary_key=True)

    def json(self):
        return {
            "site_id": self.site_id,
            "site_id": self.tag_id
        }
