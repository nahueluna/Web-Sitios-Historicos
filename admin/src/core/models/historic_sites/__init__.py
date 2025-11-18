from datetime import datetime
from sqlalchemy import func, or_
from src.core.models.search.tags import Tag
from src.core.models.historic_site_tags.hs_tags import HistoricSitesTags
from src.core.models.auth.user import usuario_favoritos
from src.core.models.historic_sites_logs import add_log, add_log_no_commit
from src.core.models.historic_site_tags import add_historic_site_tag, reset_tags, add_historic_site_tag_no_commit, reset_tags_no_commit
from src.core.models.historic_sites_state.hs_states import HistoricSitesStates
from src.core.models.historic_sites_categorie.hs_categories import HistoricSitesCategories
from src.core.database import db
from src.core.models.historic_sites.historic_sites import HistoricSites
from src.core.models.review.review import Review, ReviewStatus
from sqlalchemy import func, desc  
from math import radians, sin, cos, sqrt, atan2
from src.core.models.search.tags import Tag
from src.core.models.historic_site_tags.hs_tags import HistoricSitesTags
from src.core.models.review.review import Review, ReviewStatus
from geoalchemy2.elements import WKTElement
from geoalchemy2 import elements as geoelements, functions as geofunctions, Geography

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

def get_only_historic_site(hs_id: int):
    """Retorna el sitio historico sin logs ni categorias"""
    return db.session.get(HistoricSites, hs_id)

# Un sitio visible específico por ID con su categoría, estado y tags
def get_visible_historic_site(hs_id: int):
    return db.session.query(HistoricSites).filter(
        HistoricSites.id == hs_id,
        HistoricSites.visible == True,
        HistoricSites.delete == False
    ).first()

# Crear nuevo sitio histórico
def add_historic_site(
        site_name: str, short_description: str, long_description: str, city: str, 
        province: str, latitude: float, longitude: float, conservation_status: str, 
        inauguration_year: datetime, category: str, user_id: int, visible: bool = True, 
        tags: list = [], country: str = 'AR'
    )-> HistoricSites: 
    hs_model = HistoricSites(
        site_name=site_name, 
        short_description=short_description, 
        long_description=long_description, 
        city= city, 
        province=province, 
        country=country,
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

def set_tags(hs_id, tags):
    reset_tags_no_commit(site_id=hs_id)
    for tag_id in tags:
        add_historic_site_tag_no_commit(site_id=hs_id, tag_id=tag_id)


def log_site_edit(hs_id, user_id):
    add_log_no_commit(hs_id=hs_id, action_type="Edición", user_id=user_id) # AGREGAR EL USUARIO INVOLUCRADO (ID)

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

    total = query.group_by(HistoricSites.id).count()

    if not page is None:
        sites = query.group_by(HistoricSites.id).offset((int(page) - 1) * int(per_page)).limit(int(per_page)).all()
    else:
        sites = query.all()

    return sites, total


### --------- API PUBLICA --------- ###

def list_historic_sites_with_advanced_filters(name='', description='', city='', province='', favorites=False, tag_ids=None, lat=None, long=None, radius=None, user_id=None, order_by='registration_date', order_dir='desc', page=1, per_page=25):

    print(f"DEBUG MODEL - Filters received: name='{name}', description='{description}', city='{city}', province='{province}', tag_ids={tag_ids}")
    
    query = db.session.query(HistoricSites).filter(HistoricSites.delete == False, HistoricSites.visible == True)
    
    # Aplicar filtros con AND (todos los criterios deben coincidir)
    search_filters = []
    
    if name and name != 'None':
        search_filters.append(HistoricSites.site_name.ilike(f'%{name}%'))
    if description and description != 'None':
        search_filters.append(HistoricSites.short_description.ilike(f'%{description}%'))
    if city and city != 'None':
        query = query.filter(HistoricSites.city.ilike(f'%{city}%'))
    if province and province != 'None':
        query = query.filter(HistoricSites.province.ilike(f'{province}%'))

    # Aplicar OR a nombre y descripción
    if search_filters:
        query = query.filter(or_(*search_filters))

    if favorites and user_id:
        query = query.join(usuario_favoritos, HistoricSites.id == usuario_favoritos.c.site_id).filter(usuario_favoritos.c.user_id == user_id)

    if tag_ids:
        query = query.join(HistoricSitesTags, HistoricSites.id == HistoricSitesTags.site_id).filter(HistoricSitesTags.tag_id.in_(tag_ids))

    if lat is not None and long is not None and radius is not None:
        try:
            radius_m = float(radius) * 1000.0  # Convertir km a metros
        except Exception:
            radius_m = float(radius)

        # Construir punto central: ST_SetSRID(ST_MakePoint(lon, lat), 4326)
        center_point = func.ST_SetSRID(func.ST_MakePoint(float(long), float(lat)), 4326)

        # Construir punto del sitio desde longitude y latitude
        site_point = func.ST_SetSRID(
            func.ST_MakePoint(HistoricSites.longitude, HistoricSites.latitude),
            4326
        )

        # Usar ST_DWithin con Geography para distancias en metros
        query = query.filter(
            func.ST_DWithin(
                site_point.cast(Geography),
                center_point.cast(Geography),
                radius_m,
                use_spheroid=False
            )
        )

    if order_by == 'rating':
        subq = db.session.query(Review.historic_site_id, func.avg(Review.rating).label('avg_rating')).filter(
            Review.status == ReviewStatus.APPROVED).group_by(Review.historic_site_id).subquery()
        query = query.outerjoin(subq, HistoricSites.id == subq.c.historic_site_id).order_by(
            func.coalesce(subq.c.avg_rating, 0).desc() if order_dir == 'desc' else func.coalesce(subq.c.avg_rating,
                                                                                                 0).asc())
        query = query.order_by(HistoricSites.registration_date.desc())

        sites = query.group_by(HistoricSites.id, subq.c.avg_rating).offset((page - 1) * per_page).limit(per_page).all()
        total = query.group_by(HistoricSites.id, subq.c.avg_rating).count()
    else:
        if order_by in ['registration_date', 'site_name']:
            order_column = getattr(HistoricSites, order_by)
            if order_dir == 'desc':
                order_column = order_column.desc()
            else:
                order_column = order_column.asc()
            query = query.order_by(order_column)
        else:
            query.order_by(HistoricSites.registration_date.desc())

        sites = query.group_by(HistoricSites.id).offset((page - 1) * per_page).limit(per_page).all()
        total = query.group_by(HistoricSites.id).count()

    return sites, total


