import random
from datetime import datetime, timedelta, timezone
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites

CANTIDAD_SITIOS = 60

PROVINCIAS_ARG = [
    "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes",
    "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza",
    "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis",
    "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucumán"
]

def seed_historic_sites():
    sitios = []
    now = datetime.now(timezone.utc)
    for i in range(1, CANTIDAD_SITIOS + 1):
        sitio = HistoricSites(
            site_name=f"Sitio Histórico {i}",
            short_description=f"Descripción corta del sitio {i}",
            long_description=f"Descripción larga y detallada del sitio histórico número {i}.",
            city=f"Ciudad {random.randint(1, 100)}",
            province=random.choice(PROVINCIAS_ARG),
            latitude=random.uniform(-55.0, -21.0),
            longitude=random.uniform(-73.0, -53.0),
            registration_date=now - timedelta(days=random.randint(0, 365)),
            inauguration_year=now - timedelta(days=random.randint(365*50, 365*100)),
            visible=bool(random.getrandbits(1)),
            status_id=random.randint(1, 3),
            category_id=random.randint(1, 3),
            delete=False
        )
        sitios.append(sitio)
    db.session.add_all(sitios)
    db.session.commit()
    print(f"Seed completo: {CANTIDAD_SITIOS} sitios históricos creados.")