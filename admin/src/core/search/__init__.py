from src.core.database import db
from src.core.search.tags import  Tag

def list_tags_by_insertion_date():
    return db.session.query(Tag).order_by(Tag.inserted_at.desc()).all()

def create_tag(**kwargs):
    tag = Tag(**kwargs)
    db.session.add(tag)
    db.session.commit()

    return tag