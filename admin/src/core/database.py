
from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    return db

def reset_db():
    from src.core.models.historic_sites_state import generate_states
    from src.core.models.historic_sites_categorie import __generate_categories
    #from src.core.models.logs_actions import __generate_log_actions
    from src.core.search import tags # noqa: F401
    from src.core.models.auth.user import Usuario # noqa: F401
    print("Resetting database...")

    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("Database schema created...")
    generate_states()
    print("Historic sites states generated...")
    __generate_categories()
    print("Historic sites categories generated...")
    #__generate_log_actions()
    #print("Log actions generated...")
    print("Database reset complete...")

def seed_db():
    from src.core.models.auth.seeds import seed_usuarios
    print("🌱 Seeding database with initial data...")
    seed_usuarios()
    print("✅ Database seeding complete.")

class Base(DeclarativeBase):
    pass
