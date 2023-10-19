import os
from contextlib import asynccontextmanager

from app.controllers import (attribute_predict_coarse,
                             category_attribute_predict)
from app.services.attribute_predict_coarse import AttributePredictCoarseService
from app.services.category_attribute_predict import \
    CategoryAttributePredictService
from config import config
from extensions.minio import create_minio_connector
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.storage = await create_minio_connector(config)
    app.apc_service = AttributePredictCoarseService(storage=app.storage, config=config)
    # app.cap_service = CategoryAttributePredictService(storage=app.storage, config=config)
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
    router.include_router(attribute_predict_coarse.router, prefix=os.path.join(config['APP_API_PREFIX'], 'apc'))
    # router.include_router(category_attribute_predict.router, prefix=os.path.join(config['APP_API_PREFIX'], 'cap'))
    app.include_router(router)

    return app
