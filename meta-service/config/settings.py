from os import environ
from pydantic import BaseSettings

def convert_list_object_from_string(string):
    """Convert a string to a list of objects"""
    return [] if not string else \
        list(map(lambda x: x.strip(), string.split(",")))

class Settings(BaseSettings):
    # SECRET_KEY = environ["SECRET_KEY"]

    MODEL_SAVING_DIR = environ.get("MODEL_SAVING_DIR")
    VECTOR_SAVING_DIR = environ.get("VECTOR_SAVING_DIR")

    RASA_URL = environ.get("RASA_URL")
    META_URL = environ.get("META_URL")
    MMFASHION_URL = environ.get("MMFASHION_URL")
    
    ADMIN_MINIO_URL = environ.get("ADMIN_MINIO_URL")
    MINIO_ROOT_USER = environ.get("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD = environ.get("MINIO_ROOT_PASSWORD")
    MINIO_BUCKETS = ['rasa-service', 'meta-service', 'backend']
    IMAGE_COLORS = ['white', 'black', 'red', 'orange', 'yellow', 'blue', 'green', 'pink', 'purple']

    # DB initialization
    MONGO_ROOT_USERNAME = "admin"
    MONGO_ROOT_PASSWORD = "admin"
    MONGO_PORT = 27017
    MONGO_HOST = "chatbot-mongo"
    MONGO_AUTH_DATABASE = "admin"
    MONGO_DATABASE_URI = \
        f"mongodb://{MONGO_ROOT_USERNAME}:{MONGO_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin&readPreference=secondary&directConnection=true&ssl=false'"



class DevelopmentConfig(Settings):
    MINIO_SECURE = False
    KEYCLOAK_SECURE = False
    class Config:
        env_file = "docker/.env.development"


class ProductionConfig(Settings):
    MINIO_SECURE = False # Should be set by True (SSL/TLS)
    KEYCLOAK_SECURE = False # Should be set by True (SSL/TLS)
    class Config:
        env_file = "/docker/.env.production"