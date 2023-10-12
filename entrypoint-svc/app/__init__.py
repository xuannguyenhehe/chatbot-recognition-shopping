from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import APIRouter
from app.controllers import keycloak, chat, message, image
from app.models import create_mongo_client
from extensions.keycloak.keycloak_openid import KeycloakOpenIDConnector
from extensions.keycloak.keycloak_admin import KeycloakAdminConnector
from extensions.minio import create_minio_connector
from config import config

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
    router.include_router(keycloak.router)
    router.include_router(chat.router)
    router.include_router(message.router)
    router.include_router(image.router)
    app.include_router(router)

    return app
