from src.core.models.historic_sites.historic_sites import HistoricSites
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

def delete_category(c_id: int):
    print("id", c_id)
    # Busca la categoría por ID
    category = db.session.query(
        HistoricSitesCategories
    ).filter_by(
        id=c_id
    ).first()

    exists = db.session.query(
        HistoricSites
    ).filter_by(
        category_id=c_id
    ).first()


    if exists != None:
        raise Exception("No se puede eliminar la categoría porque está asociada a uno o más sitios históricos.")

    db.session.delete(category)
    db.session.commit()

def __generate_categories():
    categoires = ["Arquitectura", "Infraestructura", "Sitio arqueológico"]
    for category in categoires:
        hs_category = HistoricSitesCategories(category=category)
        db.session.add(hs_category)
    db.session.commit()