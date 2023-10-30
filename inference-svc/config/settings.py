from os import environ

from pydantic import BaseSettings


def convert_list_object_from_string(string):
    """Convert a string to a list of objects"""
    return [] if not string else \
        list(map(lambda x: x.strip(), string.split(",")))

class Settings(BaseSettings):
    APP_ENV: str
    APP_DEBUG: bool
    APP_PORT: int
    APP_HOST: str
    APP_API_PREFIX: str
    SERVICE_NAME: str

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    ADMIN_MINIO_URL: str
    MINIO_BUCKETS: str
    DEFAULT_BUCKET: str

    MODEL_SAVING_DIR: str

    APC_MODEL_SAVING_DIR: str
    APC_CONFIG_DIR: str

    CAP_MODEL_SAVING_DIR: str
    CAP_CONFIG_DIR: str

    IMAGE_COLORS: str

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
