from _datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    slug : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    inserted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    def __repr__(self):
       return f"<Tag(id={self.id}, name={self.name}, slug={self.slug}"


    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "inserted_at": self.inserted_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }