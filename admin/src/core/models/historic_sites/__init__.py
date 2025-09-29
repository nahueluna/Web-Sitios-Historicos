from datetime import datetime
from src.core.models.historic_sites_state.hs_states import HistoricSitesStates
from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories
from src.core.models.historic_sites_logs.hs_logs import HistoricSitesLogs
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites  

# Consulta para todos los sitios con su categoría
def list_all_historic_sites(): 
    return db.session.query(
        HistoricSites
    ).all()

# Solo sitios visibles con su categoría y estado
def list_visible_historic_sites(): 
    return db.session.query(
        HistoricSites
    ).filter(
        HistoricSites.visible == True
    ).all()

# Un sitio visible específico por ID con todos sus logs y su categoría
def get_historic_site(hs_id: int): 
    return db.session.query(
        HistoricSites, HistoricSitesCategories, HistoricSitesStates
    ).filter(
        HistoricSites.id == hs_id,
    ).join(
        HistoricSitesCategories, HistoricSites.category_id == HistoricSitesCategories.id
    ).join(
        HistoricSitesStates, HistoricSites.status_id == HistoricSitesStates.id
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
        status_id=conservation_status, 
        inauguration_year=inauguration_year, 
        category_id=category,
        visible=visible)
    db.session.add(hs_model)
    db.session.commit()
    return hs_model

def edit_historic_site(
        hs_id: int, site_name: str, short_description: str, long_description: str, 
        city: str, province: str, latitude: float, longitude: float, 
        conservation_status: str, inauguration_year: datetime, category: str, 
        registration_date: datetime, visible: bool = True
    ) -> HistoricSites:
    hs_model = db.session.query(HistoricSites).filter(HistoricSites.id == hs_id).first()
    if not hs_model:
        return None
    hs_model.site_name = site_name
    hs_model.short_description = short_description
    hs_model.long_description = long_description
    hs_model.city = city
    hs_model.province = province
    hs_model.latitude = latitude
    hs_model.longitude = longitude
    hs_model.status_id = conservation_status
    hs_model.inauguration_year = inauguration_year
    hs_model.category_id = category
    hs_model.registration_date = registration_date
    hs_model.visible = visible

    db.session.commit()
    return hs_model