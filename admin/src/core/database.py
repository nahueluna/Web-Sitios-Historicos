from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()

class Base(DeclarativeBase):
    pass

def init_app(app):
    db.init_app(app)
    return db

def reset_db():
    from src.core.models import test  # noqa: F401 
    print("Resetting database...")
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("Database reset complete.")


def seed_db():
    from src.core.board.seeds import run_seeds
    print("🌱 Seeding database with initial data...")
    run_seeds()
    print("✅ Database seeding complete.")

