from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    TESTING = False
    SECRET_KEY = environ.get("SECRET_KEY")
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }

class ProductionConfig(Config):

    # Minio
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    MINIO_BUCKET = "grupo03"

    SQLALCHEMY_ENGINES = {
        'default': environ.get("DATABASE_URL")}


class DevelopmentConfig(Config):
    DB_USER = environ.get("DB_USER")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_PORT = environ.get("DB_PORT", "5432")
    DB_NAME = environ.get("DB_NAME", "grupo03")
    DB_SCHEME = environ.get("DB_SCHEME", "postgresql+psycopg2")

    # Minio
    MINIO_SERVER = environ.get("MINIO_SERVER_DEV", "localhost:9000");
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY_DEV", "minioadmin")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY_DEV", "minioadmin")
    MINIO_SECURE = environ.get("MINIO_SECURE_DEV", False)
    MINIO_BUCKET = "grupo03"

    SQLALCHEMY_ENGINES = {
        'default': f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    }

class TestingConfig(Config):
    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
