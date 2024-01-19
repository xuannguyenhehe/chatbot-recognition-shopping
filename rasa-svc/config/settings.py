from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str
    APP_DEBUG: bool
    APP_PORT: int
    APP_HOST: str
    APP_API_PREFIX: str
    SERVICE_NAME: str

    CHECKPOINT_PATH: str
    RASA_CFG: str
    DOMAIN_CFG: str
    NLU_CFG: str
    SYNONYM_CFG: str
    RESPONSES_CFG: str
    RULES_CFG: str
    STORIES_CFG: str

    MINIO_BUCKETS: str
    ADMIN_MINIO_URL: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    DEFAULT_BUCKET: str


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
