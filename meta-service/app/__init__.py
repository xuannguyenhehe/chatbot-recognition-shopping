import os
from contextlib import asynccontextmanager

from app.controllers import image, inference
from app.models import create_mongo_client
from app.services.inference import InferenceService
from config import config
from extensions.keycloak.keycloak_admin import KeycloakAdminConnector
from extensions.keycloak.keycloak_openid import KeycloakOpenIDConnector
from extensions.minio import create_minio_connector
from extensions.vector import create_vector_search
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.db = await create_mongo_client(config)
    app.storage = await create_minio_connector(config)
    app.vector_search = await create_vector_search(config)
    app.inference_server = InferenceService(config, app.storage, app.vector_search, app.db)
    app.kc_openid = KeycloakOpenIDConnector()
    app.kc_openid.init_app(config)
    app.kc_admin = KeycloakAdminConnector()
    app.kc_admin.init_app(config)
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
    router.include_router(inference.router, prefix=os.path.join(config['APP_API_PREFIX'], 'inference'))
    router.include_router(image.router, prefix=os.path.join(config['APP_API_PREFIX'], 'image'))
    app.include_router(router)

    return app
