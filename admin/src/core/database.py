from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    return db

def reset_db():
    from src.core.models.historic_sites_state import generate_states
    from src.core.models.historic_sites_categorie import generate_categories

    print("Resetting database...")
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("Database schema created...")
    generate_states()
    print("Historic sites states generated...")
    generate_categories()
    print("Historic sites categories generated...")
    print("Database reset complete...")

class Base(DeclarativeBase):
    pass