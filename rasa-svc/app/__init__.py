import os
from contextlib import asynccontextmanager

from app.controllers import inference
from app.services.inference import InferenceService
from config import config
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.rasa_service = InferenceService(config)
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
    app.include_router(router)

    return app
