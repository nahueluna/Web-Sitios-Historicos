from typing import List
from src.core.database import db
from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories  
from sqlalchemy.orm import joinedload

# Traer todas las categorías
def list_historic_sites_categorie()-> List[HistoricSitesCategories]: 
    return db.session.query(
        HistoricSitesCategories
    ).all()

# Traer una categoría con sus sitios históricos relacionados
def get_categorie_with_hs(categoria_id: int)-> HistoricSitesCategories:
    return db.session.query(
        HistoricSitesCategories
    ).options(
        joinedload(
            HistoricSitesCategories.sites
        )
    ).filter(
        HistoricSitesCategories.id == categoria_id
    ).first()

# Agregar una categoría
def add_category(category_name: str)-> HistoricSitesCategories: 
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