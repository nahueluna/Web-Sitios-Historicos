from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime, timezone

class LogActions(Base):
    __tablename__ = "log_actions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    action: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self): return f"{self.action}"

    def __init__(self, action: str):
        self.action = action

    