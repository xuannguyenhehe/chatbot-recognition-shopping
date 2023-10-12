from os import environ
from pydantic import BaseSettings

def convert_list_object_from_string(string):
    """Convert a string to a list of objects"""
    return [] if not string else \
        list(map(lambda x: x.strip(), string.split(",")))

class Settings(BaseSettings):
    ADMIN_MINIO_URL: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_REGION: str
    MINIO_BUCKETS: str
    
    APC_MODEL_SAVING_DIR: str
    APC_CONFIG_DIR: str

    CAP_MODEL_SAVING_DIR: str
    CAP_CONFIG_DIR: str


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