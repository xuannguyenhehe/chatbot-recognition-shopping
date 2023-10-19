from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str
    APP_DEBUG: bool
    APP_PORT: int
    APP_HOST: str
    APP_API_PREFIX: str
    SERVICE_NAME: str

    KEYCLOAK_SECRET_KEY: str
    KEYCLOAK_ADMIN_USERNAME: str
    KEYCLOAK_ADMIN_PASSWORD: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_URL: str
    REALMS: str

    MINIO_BUCKETS: str
    ADMIN_MINIO_URL: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    DEFAULT_BUCKET: str

    # DB initialization
    MONGO_ROOT_USERNAME: str
    MONGO_ROOT_PASSWORD: str
    MONGO_PORT: int
    MONGO_HOST: str
    MONGO_AUTH_DATABASE: str

    # OTHER
    META_URL: str
    RASA_URL: str
    MMFASHION_URL: str

class DevelopmentConfig(Settings):
    class Config:
        env_file = "docker/.env.development"


class ProductionConfig(Settings):
    class Config:
        env_file = "/docker/.env.production"