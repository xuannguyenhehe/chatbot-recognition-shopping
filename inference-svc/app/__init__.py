import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import color_inference, meta_inference, attribute_inference, category_attribute_inference
from app.services.attribute_inference import AttributePredictCoarseService
from app.services.category_attribute_inference import \
    CategoryAttributePredictService
from app.services.color_inference import ColorInferenceService
from app.services.meta_inference import MetaInferenceService
from config import config
from extensions.minio import create_minio_connector


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.storage = await create_minio_connector(config)
    app.meta_inference_server = MetaInferenceService(config, app.storage)
    app.color_inference_server = ColorInferenceService(config, app.storage)
    app.attribute_inference_server = AttributePredictCoarseService(storage=app.storage, config=config)
    app.category_attribute_inference_server = CategoryAttributePredictService(storage=app.storage, config=config)
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
    router.include_router(meta_inference.router, prefix=os.path.join(config['APP_API_PREFIX'], 'meta-inference'))
    router.include_router(color_inference.router, prefix=os.path.join(config['APP_API_PREFIX'], 'color-inference'))
    router.include_router(attribute_inference.router, prefix=os.path.join(config['APP_API_PREFIX'], 'attribute-inference'))
    router.include_router(category_attribute_inference.router, prefix=os.path.join(config['APP_API_PREFIX'], 'category-attribute-inference'))
    app.include_router(router)

    return app
