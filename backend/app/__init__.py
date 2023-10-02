from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import APIRouter
from app.controllers import message, user, chat, image
from app.models import create_mongo_client
from extensions.minio import create_minio_connector
from config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_mongo_client()
    await create_minio_connector()
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
    router.include_router(message.router)
    router.include_router(image.router)
    router.include_router(user.router)
    router.include_router(chat.router)
    app.include_router(router)

    return app
