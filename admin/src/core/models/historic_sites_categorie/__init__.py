from src.core.database import db
from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories  

def list_historic_sites_categorie(): return db.session.query(HistoricSitesCategories).all()

def generate_categories():
    categoires = ["Arquitectura", "Infraestructura", "Sitio arqueológico"]
    for category in categoires:
        hs_category = HistoricSitesCategories(category=category)
        db.session.add(hs_category)
    db.session.commit()