from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites  

def list_all_historic_sites(): 
    return db.session.query(HistoricSites).all()

def list_historic_sites(): 
    return db.session.query(HistoricSites).filter(HistoricSites.visible == True).all()

def get_historic_site_by_id(id: int): 
    return db.session.query(HistoricSites).filter(HistoricSites.id == id and HistoricSites.visible == True).first()

def add_historic_site(**keywords)-> HistoricSites: 
    historic_site = HistoricSites(**keywords)
    db.session.add(historic_site)
    db.session.commit()
    return historic_site