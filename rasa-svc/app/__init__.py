import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import inference, train
from app.services.inference import InferenceService
from app.services.train import TrainService
from config import config
from extensions.minio import create_minio_connector


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.inference_service = InferenceService(config)
    app.storage = await create_minio_connector(config)
    app.train_service = TrainService(config, app.storage)
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
    router.include_router(inference.router, prefix=os.path.join(config['APP_API_PREFIX'], 'answer'))
    router.include_router(train.router, prefix=os.path.join(config['APP_API_PREFIX'], 'train'))
    app.include_router(router)

    return app
