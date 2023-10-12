from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from contextlib import asynccontextmanager
from app.controllers import inference, image
from extensions.minio import create_minio_connector
from extensions.vector import create_vector_search
from app.models import create_mongo_client
from config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.db = await create_mongo_client(config)
    app.storage = await create_minio_connector(config)
    app.vector_search = await create_vector_search(config)
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
    router.include_router(inference.router)
    router.include_router(image.router)
    app.include_router(router)

    return app
