from datetime import datetime
from src.core.models.search.tags import Tag
from src.core.models.historic_site_tags.hs_tags import HistoricSitesTags
from src.core.models.historic_sites_logs import add_log
from src.core.models.historic_site_tags import add_historic_site_tag, reset_tags
from src.core.models.historic_sites_state.hs_states import HistoricSitesStates
from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites  

# Consulta para todos los sitios con su categoría
def list_all_historic_sites(): 
    return db.session.query(
        HistoricSites
    ).filter(
        HistoricSites.delete == False
    ).order_by(HistoricSites.site_name).all()

# Solo sitios visibles con su categoría y estado
def list_visible_historic_sites(): 
    return db.session.query(
        HistoricSites
    ).filter(
        HistoricSites.visible == True, HistoricSites.delete == False
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
        inauguration_year: datetime, category: str, user_id: int, visible: bool = True, tags: list = [],
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

    db.session.flush() 

    add_log(hs_id=hs_model.id, action_type="Creación", user_id= user_id) # AGREGAR EL USUARIO INVOLUCRADO (ID)

    for tag_id in tags:
        add_historic_site_tag(site_id=hs_model.id, tag_id=tag_id)

    db.session.commit()
    return hs_model

def edit_historic_site(
        hs_id: int, site_name: str, short_description: str, long_description: str, 
        city: str, province: str, latitude: float, longitude: float, 
        conservation_status: str, inauguration_year: datetime, category: str, 
        user_id: int, visible: bool = True, tags: list = []
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
    hs_model.visible = visible

    add_log(hs_id=hs_id, action_type="Edición", user_id=user_id) # AGREGAR EL USUARIO INVOLUCRADO (ID)
    reset_tags(site_id=hs_id)
    for tag_id in tags:
        add_historic_site_tag(site_id=hs_id, tag_id=tag_id)

    db.session.commit()
    return hs_model

def delete_histoirc_site(hs_id: int, user_id: int):
    hs_model = db.session.query(HistoricSites).filter(HistoricSites.id == hs_id).first()
    if not hs_model:
        return None
    hs_model.delete = True

    add_log(hs_id=hs_id, action_type="Eliminación", user_id=user_id) # AGREGAR EL USUARIO INVOLUCRADO (ID)

    db.session.commit()
    return hs_model

def list_historic_sites_with_filters(q='', city='', province='', tags=None, status='', date_from='', date_to='', visible='false', order_by='site_name', order_dir='asc', page=1, per_page=25):
    query = db.session.query(
        HistoricSites
    ).filter(
        HistoricSites.delete == False
    )

    if q:
        query = query.filter(
            HistoricSites.site_name.ilike(f'%{q}%') |
            HistoricSites.short_description.ilike(f'%{q}%')
        )

    if city:
        query = query.filter(HistoricSites.city.ilike(f'%{city}%'))

    if province:
        query = query.filter(HistoricSites.province.ilike(f'{province}'))

    if tags:
        query = (query.join(HistoricSitesTags, HistoricSites.id == HistoricSitesTags.site_id)
                 .filter(HistoricSitesTags.tag_id.in_(tags)))

    if status:
        query = (query.join(HistoricSitesStates, HistoricSites.status_id == HistoricSitesStates.id)
                 .filter(HistoricSitesStates.state == status))

    if date_from:
        try:
            date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(HistoricSites.registration_date >= date_from_parsed)
        except ValueError:
            pass

    if date_to:
        try:
            date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(HistoricSites.registration_date <= date_to_parsed)
        except ValueError:
            pass

    if visible.lower() == 'true':
        query = query.filter(HistoricSites.visible == True)

    if order_by in ['site_name', 'city', 'registration_date']:
        order_column = getattr(HistoricSites, order_by)
        if order_dir == 'desc':
            order_column = order_column.desc()
        else:
            order_column = order_column.asc()
        query = query.order_by(order_column)

    total = query.count()

    if not page is None:
        sites = query.offset((int(page) - 1) * int(per_page)).limit(int(per_page)).all()
    else:
        sites = query.all()

    return sites, total