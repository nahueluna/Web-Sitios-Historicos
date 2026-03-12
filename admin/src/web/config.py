from os import environ
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


# Variables requeridas por entorno (se validan en create_app, no al importar)
_REQUIRED_VARS = {
    "base": ["BACKEND_SECRET_KEY", "BACKEND_JWT_SECRET_KEY"],
    "production": [
        "DATABASE_URL", "MINIO_SERVER", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY",
        "CORS_ALLOWED_ORIGINS", "GOOGLE_CLIENT_ID",
    ],
}


def validate_env(env_name):
    """Validate that all required environment variables are set for the given env."""
    missing = [v for v in _REQUIRED_VARS["base"] if not environ.get(v)]
    if env_name in _REQUIRED_VARS:
        missing += [v for v in _REQUIRED_VARS[env_name] if not environ.get(v)]
    if missing:
        raise RuntimeError(
            f"Variables de entorno requeridas no configuradas: {', '.join(missing)}"
        )


class Config:
    TESTING = False
    SECRET_KEY = environ.get("BACKEND_SECRET_KEY")
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }

    JWT_SECRET_KEY = environ.get('BACKEND_JWT_SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    # CORS — orígenes permitidos (separados por coma)
    CORS_ALLOWED_ORIGINS = environ.get(
        "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    )

    # Google OAuth
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")


class ProductionConfig(Config):

    # Minio
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    MINIO_BUCKET = environ.get("MINIO_BUCKET_NAME", "grupo03")

    # Render provee DATABASE_URL con esquema postgres:// pero SQLAlchemy 2
    # requiere postgresql://. Se corrige automáticamente.
    _db_url = environ.get("DATABASE_URL", "")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_ENGINES = {
        'default': _db_url,
    }


class DevelopmentConfig(Config):
    DB_USER = environ.get("DB_USER")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_PORT = environ.get("DB_PORT", "5432")
    DB_NAME = environ.get("DB_NAME", "grupo03")
    DB_SCHEME = environ.get("DB_SCHEME", "postgresql+psycopg2")

    # Minio
    MINIO_SERVER = environ.get("MINIO_SERVER_DEV", "localhost:9000")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY_DEV", "minioadmin")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY_DEV", "minioadmin")
    MINIO_SECURE = str(environ.get("MINIO_SECURE_DEV", "false")).lower() == "true"
    MINIO_BUCKET = environ.get("MINIO_BUCKET_NAME_DEV", "grupo03")

    SQLALCHEMY_ENGINES = {
        'default': f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    }


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = environ.get("BACKEND_SECRET_KEY", "test-secret-key")
    JWT_SECRET_KEY = environ.get("BACKEND_JWT_SECRET_KEY", "test-jwt-secret-key")


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
