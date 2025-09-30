from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    return db

def reset_db():
    print("Resetting database...")
    from src.core.search import tags # noqa: F401
    from src.core.models.auth.user import Usuario # noqa: F401

    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("Database reset complete.")

def seed_db():
    from src.core.models.auth.seeds import seed_usuarios
    print("🌱 Seeding database with initial data...")
    seed_usuarios()
    print("✅ Database seeding complete.")

class Base(DeclarativeBase):
    pass
