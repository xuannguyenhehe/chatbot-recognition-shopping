from os import environ
from pydantic import BaseSettings

def convert_list_object_from_string(string):
    """Convert a string to a list of objects"""
    return [] if not string else \
        list(map(lambda x: x.strip(), string.split(",")))

class Settings(BaseSettings):
    # SECRET_KEY = environ["SECRET_KEY"]

    MODEL_SAVING_DIR = environ.get("MODEL_SAVING_DIR")

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