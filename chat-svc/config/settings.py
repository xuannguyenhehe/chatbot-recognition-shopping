from os import environ
from pydantic import BaseSettings

def convert_list_object_from_string(string):
    """Convert a string to a list of objects"""
    return [] if not string else \
        list(map(lambda x: x.strip(), string.split(",")))

class Settings(BaseSettings):
    # SECRET_KEY = environ["SECRET_KEY"]

    # DB initialization
    MONGO_ROOT_USERNAME = "admin"
    MONGO_ROOT_PASSWORD = "admin"
    MONGO_PORT = 27017
    MONGO_HOST = "chatbot-mongo"
    MONGO_AUTH_DATABASE = "admin"
    MONGO_DATABASE_URI = \
        f"mongodb://{MONGO_ROOT_USERNAME}:{MONGO_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin&readPreference=secondary&directConnection=true&ssl=false'"

    ADMIN_MINIO_URL = environ["ADMIN_MINIO_URL"]
    MINIO_ROOT_USER = environ["MINIO_ROOT_USER"]
    MINIO_ROOT_PASSWORD = environ["MINIO_ROOT_PASSWORD"]
    MINIO_REGION = environ.get("MINIO_REGION")
    MINIO_BUCKETS = ['rasa-service', 'meta-service', 'backend']
    # print("MINIO_BUCKETS", MINIO_BUCKETS)

    RASA_URL = environ.get("RASA_URL")
    META_URL = environ.get("META_URL")


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