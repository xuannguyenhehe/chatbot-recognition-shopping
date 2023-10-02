from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from contextlib import asynccontextmanager
from app.controllers import inference, image
from extensions.minio import create_minio_connector
from extensions.vector import create_vector_search
from app.models import create_mongo_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_dbname = "meta-service"
    app.state.storage = await create_minio_connector()
    app.state.db = await create_mongo_client(mongo_dbname)
    app.state.vector_search = await create_vector_search()
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
    # router.include_router(image.router)
    app.include_router(router)

    return app
