from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    TESTING = False
    SECRET_KEY = "you_secret_key"
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    SQLALCHEMY_ENGINES = {
        'default': environ.get("DATABASE_URL")}


class DevelopmentConfig(Config):
    SECRET_KEY = "you_development_secret_key"
    
    DB_USER = environ.get("DB_USER")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo03"
    DB_SCHEME = "postgresql+psycopg2"

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