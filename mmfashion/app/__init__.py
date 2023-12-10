from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (attribute_predict_coarse,
                             category_attribute_predict)
from app.services.attribute_predict_coarse import AttributePredictCoarseService
from app.services.category_attribute_predict import \
    CategoryAttributePredictService
from extensions.minio import create_minio_connector


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.storage = await create_minio_connector()
    app.state.apc_service = AttributePredictCoarseService(
        storage=app.state.storage,
    )
    app.state.cap_service = CategoryAttributePredictService(
        storage=app.state.storage,
    )
    yield

def create_app():
    app = FastAPI(
        lifespan=lifespan,
    )
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
    router.include_router(attribute_predict_coarse.router)
    router.include_router(category_attribute_predict.router)
    app.include_router(router)

    return app
