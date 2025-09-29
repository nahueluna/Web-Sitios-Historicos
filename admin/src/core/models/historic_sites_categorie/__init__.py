from src.core.database import db
from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories  

# Traer todas las categorías
def list_historic_sites_categorie(): 
    return db.session.query(
        HistoricSitesCategories
    ).all()

# Agregar una categoría
def add_category(category_name: str): 
    category_model = db.session.query(
        HistoricSitesCategories
    ).filter(
        HistoricSitesCategories.category == category_name
    ).first()

    if category_model:
        raise Exception("La categoria ya existe.")

    category_model = HistoricSitesCategories(category=category_name)
    db.session.add(category_model)
    db.session.commit()
    return category_model

def __generate_categories():
    categoires = ["Arquitectura", "Infraestructura", "Sitio arqueológico"]
    for category in categoires:
        hs_category = HistoricSitesCategories(category=category)
        db.session.add(hs_category)
    db.session.commit()