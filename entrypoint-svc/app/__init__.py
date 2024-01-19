import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import chat, image, keycloak, message, qa, rasa
from app.models import create_mongo_client
from config import config
from extensions.keycloak.keycloak_admin import KeycloakAdminConnector
from extensions.keycloak.keycloak_openid import KeycloakOpenIDConnector
from extensions.minio import create_minio_connector


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.db = await create_mongo_client(config)
    app.kc_openid = KeycloakOpenIDConnector()
    app.kc_openid.init_app(config)
    app.kc_admin = KeycloakAdminConnector()
    app.kc_admin.init_app(config)
    app.storage = await create_minio_connector(config)
    yield

def create_app():
    app = FastAPI(lifespan=lifespan)
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import a module / component using its blueprint handler variable
    router = APIRouter()
    router.include_router(keycloak.router, prefix=os.path.join(config['APP_API_PREFIX'], 'keycloak'))
    router.include_router(chat.router, prefix=os.path.join(config['APP_API_PREFIX'], 'chat'))
    router.include_router(message.router, prefix=os.path.join(config['APP_API_PREFIX'], 'message'))
    router.include_router(image.router, prefix=os.path.join(config['APP_API_PREFIX'], 'image'))
    router.include_router(qa.router, prefix=os.path.join(config['APP_API_PREFIX'], 'qa'))
    router.include_router(rasa.router, prefix=os.path.join(config['APP_API_PREFIX'], 'rasa'))
    app.include_router(router)

    return app
