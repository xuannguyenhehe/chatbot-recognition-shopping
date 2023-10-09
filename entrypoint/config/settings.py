from pydantic import BaseSettings


class Settings(BaseSettings):
    KEYCLOAK_SECRET_KEY: str
    KEYCLOAK_ADMIN_USERNAME: str
    KEYCLOAK_ADMIN_PASSWORD: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_URL: str
    REALMS: str

    # DB initialization
    MONGO_ROOT_USERNAME = "admin"
    MONGO_ROOT_PASSWORD = "admin"
    MONGO_PORT = 27017
    MONGO_HOST = "chatbot-mongo"
    MONGO_AUTH_DATABASE = "admin"
    MONGO_DATABASE_URI = \
        f"mongodb://{MONGO_ROOT_USERNAME}:{MONGO_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin&readPreference=secondary&directConnection=true&ssl=false'"


class DevelopmentConfig(Settings):
    class Config:
        env_file = "docker/.env.development"


class ProductionConfig(Settings):
    class Config:
        env_file = "/docker/.env.production"