from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput, StockInput
from app.services.inference import InferenceService
from app.services.image import ImageService
from app.utils.repsonse.result import handle_result

router = APIRouter()


@router.post("/")
async def get_recommend(input: InferenceInput, request: Request):
    response = InferenceService(
        vector_search=request.app.vector_search,
        storage=request.app.storage
    ).get_result(input)
    return handle_result(response)


@router.post("/stock")
async def get_stock(input: StockInput, request: Request):
    response = ImageService(
        vector_search=request.app.vector_search,
        storage=request.app.storage,
        db=request.app.db,
    ).get_stock(input.username, input.label)
    return handle_result(response)
