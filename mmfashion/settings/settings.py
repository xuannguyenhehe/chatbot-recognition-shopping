from os import environ

from pydantic import BaseSettings


def convert_list_object_from_string(string):
    """Convert a string to a list of objects"""
    return [] if not string else \
        list(map(lambda x: x.strip(), string.split(",")))

class Settings(BaseSettings):
    # SECRET_KEY = environ["SECRET_KEY"]

    ADMIN_MINIO_URL = environ["ADMIN_MINIO_URL"]
    MINIO_ROOT_USER = environ["MINIO_ROOT_USER"]
    MINIO_ROOT_PASSWORD = environ["MINIO_ROOT_PASSWORD"]
    MINIO_REGION = environ.get("MINIO_REGION")
    MINIO_BUCKETS = convert_list_object_from_string(environ["LS_MINIO_BUCKETS"])
    
    APC_MODEL_SAVING_DIR=environ["APC_MODEL_SAVING_DIR"]
    APC_CONFIG_DIR=environ["APC_CONFIG_DIR"]

    CAP_MODEL_SAVING_DIR=environ["CAP_MODEL_SAVING_DIR"]
    CAP_CONFIG_DIR=environ["CAP_CONFIG_DIR"]

    FPS_MODEL_SAVING_DIR=environ["FPS_MODEL_SAVING_DIR"]
    FPS_CONFIG_DIR=environ["FPS_CONFIG_DIR"]


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
