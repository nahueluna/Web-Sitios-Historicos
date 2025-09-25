from datetime import datetime
from src.core.models.historic_sites_logs.hs_logs import HistoricSitesLogs
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites  

from sqlalchemy.orm import joinedload

# Consulta para todos los sitios con su categoría
def list_all_historic_sites(): 
    return db.session.query(
        HistoricSites
    ).options(
        joinedload(
            HistoricSites.category_rel
        )
    ).all()

# Solo sitios visibles con su categoría
def list_visible_historic_sites(): 
    return db.session.query(
        HistoricSites
    ).filter(
        HistoricSites.visible == True
    ).options(
        joinedload(
            HistoricSites.category_rel
        )
    ).all()

# Un sitio visible específico por ID con todos sus logs y su categoría
def get_historic_site(hs_id: int): 
    return db.session.query(
        HistoricSites
    ).filter(
        HistoricSites.id == hs_id,
        HistoricSites.visible == True
    ).options(
        joinedload(HistoricSites.category_rel),
        joinedload(HistoricSites.logs)
    ).first()

# Un sitio no visible específico por ID con todos sus logs y su categoría
def get_historic_site(hs_id: int): 
    return db.session.query(
        HistoricSites
    ).filter(
        HistoricSites.id == hs_id, 
        HistoricSites.visible == False
    ).options(
        joinedload(HistoricSites.category_rel),
        joinedload(HistoricSites.logs)
    ).first()

# Crear nuevo sitio histórico
def add_historic_site(
        site_name: str, short_description: str, long_description: str, city: str, 
        province: str, latitude: float, longitude: float, conservation_status: str, 
        inauguration_year: datetime, category: str, visible: bool = True
    )-> HistoricSites: 
    hs_model = HistoricSites(
        site_name=site_name, 
        short_description=short_description, 
        long_description=long_description, 
        city= city, 
        province=province, 
        latitude=latitude, 
        longitude=longitude, 
        status_id=1, ## CAMBIAR
        inauguration_year=inauguration_year, 
        category_id=1, ## CAMBIAR
        visible=visible)
    db.session.add(hs_model)
    db.session.commit()
    return hs_model