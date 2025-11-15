from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, DateTime, func, Integer
from src.core.database import Base
from datetime import datetime

# Modelo Imagen
class Image(Base):
    __tablename__ = "imagenes"
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    desc: Mapped[str] = mapped_column(String(300), nullable=False)
    orden: Mapped[int] = mapped_column(Integer, nullable=False)
    sitio: Mapped[int] = mapped_column(ForeignKey('historic_sites.id'), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def json(self):
        return {
            "nombre": self.nombre,
            "titulo": self.titulo,
            "desc": self.desc,
            "orden": self.orden,
            "sitio": self.sitio,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "url": self.url if self.url else None
        }
