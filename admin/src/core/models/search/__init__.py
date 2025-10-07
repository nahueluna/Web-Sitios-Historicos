from src.core.database import db
from src.core.models.search.tags import Tag

def list_tags(order_by, order_dir, query, page=1, per_page=10):
    column = getattr(Tag, order_by)
    if not column:
        raise ValueError("Invalid order_by field")
    if order_dir == 'desc':
        column = column.desc()
    else:
        column = column.asc()

    query = db.session.query(Tag).filter(Tag.name.ilike(f"%{query}%")).order_by(column)
    total = query.count()
    tags_list = query.offset((page-1) * per_page).limit(per_page).all()

    return tags_list, total

def get_tag_by_id(tag_id):
    return db.session.query(Tag).filter(Tag.id == tag_id).first()

def create_tag(**kwargs):
    tag = Tag(**kwargs)
    db.session.add(tag)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return tag

def update_tag_name(tag_id, new_name, new_slug):
    tag = db.session.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = new_name
        tag.slug = new_slug

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    return tag

def remove_tag(tag_id):
    tag = db.session.query(Tag).filter(Tag.id == tag_id).first()

    if tag:
        db.session.delete(tag)
        db.session.commit()
        return True

    return False

def tag_has_association_with_site(tag_id):
    from src.core.models.historic_site_tags.hs_tags import HistoricSitesTags

    association = db.session.query(HistoricSitesTags).filter(HistoricSitesTags.tag_id == tag_id).first()
    return association is not None

def get_all_tags():
    return db.session.query(Tag).all()