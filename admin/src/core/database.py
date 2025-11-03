from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()

class Base(DeclarativeBase):
    pass

def init_app(app):
    db.init_app(app)
    return db

def reset_db():
    from src.core.models.historic_sites_state import generate_states # noqa: F401
    from src.core.models.historic_sites_categorie import __generate_categories # noqa: F401
    #from src.core.models.logs_actions import __generate_log_actions
    from src.core.models.search import tags # noqa: F401
    from src.core.models.auth.user import Usuario # noqa: F401
    from src.core.models.auth.role_permission import Role, Permission, RolePermission # noqa: F
    from src.core.models.feature_flag import initialize_default_flags # noqa: F401
    from src.core.models.review import Review # noqa: F401
    

    print("Resetting database...")

    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("Database schema created...")
    generate_states()
    print("Historic sites states generated...")
    __generate_categories()
    print("Historic sites categories generated...")
    initialize_default_flags()
    print("Feature flags initialized...")
    #__generate_log_actions()
    #print("Log actions generated...")
    print("Database reset complete...")

def seed_db():
    from src.core.models.auth.seeds import seed_usuarios
    print("🌱 Seeding database with initial data...")
    seed_usuarios()
    seed_db_sites()
    seed_db_reviews()
    print("✅ Database seeding complete.")


def seed_db_user():
    from src.core.models.seeds_user import run_seeds
    print("🌱 Seeding database with user data...")
    run_seeds()
    print("✅ User database seeding complete.")

def seed_db_sites():
    from src.core.models.historic_sites.seeds import seed_historic_sites
    from src.core.models.search.seeds import seed_tags, seed_historic_sites_tags
    print("🌱 Seeding database with historic sites data...")
    seed_tags()
    seed_historic_sites()
    seed_historic_sites_tags()
    print("✅ Historic sites database seeding complete.")

def seed_db_reviews():
    from src.core.models.review.seeds import seed_reviews
    print("🌱 Seeding database with reviews data...")
    seed_reviews()
    print("✅ Reviews database seeding complete.")