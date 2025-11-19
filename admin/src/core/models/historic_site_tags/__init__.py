from src.core.models.search.tags import Tag
from src.core.models.historic_site_tags.hs_tags import HistoricSitesTags
from src.core.database import db


def add_historic_site_tag(site_id: int, tag_id: int):
    tag_model = HistoricSitesTags(
        site_id=site_id,
        tag_id=tag_id
    )
    db.session.add(tag_model)
    db.session.commit()
    return tag_model

def add_historic_site_tag_no_commit(site_id: int, tag_id: int):
    tag_model = HistoricSitesTags(
        site_id=site_id,
        tag_id=tag_id
    )
    db.session.add(tag_model)
    db.session.commit()
    return tag_model

def reset_tags(site_id: int):
    db.session.query(HistoricSitesTags).filter(HistoricSitesTags.site_id == site_id).delete()
    db.session.commit()

def reset_tags_no_commit(site_id: int):
    db.session.query(HistoricSitesTags).filter(HistoricSitesTags.site_id == site_id).delete()

def get_tags_by_site(site_id: int):
    return db.session.query(
        Tag
    ).join(
        HistoricSitesTags,  HistoricSitesTags.tag_id == Tag.id
    ).filter(
        HistoricSitesTags.site_id == site_id
    ).all()

def get_tag_by_name(tag_name: str):
    return db.session.query(
        Tag
    ).filter(
        Tag.name == tag_name
    ).first()
