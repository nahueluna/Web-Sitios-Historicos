from src.core.database import db
from src.core.search.tags import  Tag

def list_tags_by_update_date():
    return db.session.query(Tag).order_by(Tag.updated_at.desc()).all()

def get_tag_by_id(tag_id):
    return db.session.query(Tag).filter(Tag.id == tag_id).first()

def create_tag(**kwargs):
    tag = Tag(**kwargs)
    db.session.add(tag)
    db.session.commit()

    return tag

def update_tag_name(tag_id, new_name, new_slug):
    tag = db.session.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = new_name
        tag.slug = new_slug
        db.session.commit()
    return tag

def remove_tag(tag_id):
    tag = db.session.query(Tag).filter(Tag.id == tag_id).first()

    if tag:
        db.session.delete(tag)
        db.session.commit()
        return True

    return False