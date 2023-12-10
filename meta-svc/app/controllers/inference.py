from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput
from app.services.inference import InferenceService
from app.utils.repsonse.result import handle_result

router = APIRouter()


@router.post("/")
async def get_recommend(input: InferenceInput, request: Request):
    response = InferenceService(
        vector_search=request.app.vector_search,
        storage=request.app.storage
    ).get_result(input)
    return handle_result(response)
