import os

from settings.settings import DevelopmentConfig, ProductionConfig

environment = os.getenv("APP_ENV", default="development")
config = DevelopmentConfig() \
    if environment == "development" else ProductionConfig()
config = config.dict()
