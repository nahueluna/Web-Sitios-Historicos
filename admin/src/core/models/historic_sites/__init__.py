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
def add_historic_site(**keywords)-> HistoricSites: 
    hs_model = HistoricSites(**keywords)
    db.session.add(hs_model)
    db.session.commit()
    return hs_model