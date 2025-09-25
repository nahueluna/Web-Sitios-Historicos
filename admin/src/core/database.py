from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()

class Base(DeclarativeBase):
    pass

def init_app(app):
    db.init_app(app)
    return db

def reset_db():
    from src.core.models.auth import user, role_permission  # noqa: F401 
    print("Resetting database...")
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("Database reset complete.")


def seed_db_user():
    from src.core.models.seeds_user import run_seeds
    print("🌱 Seeding database with user data...")
    run_seeds()
    print("✅ User database seeding complete.")

