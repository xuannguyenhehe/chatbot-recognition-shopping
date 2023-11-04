from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput
from app.services.inference import InferenceService
from app.utils.repsonse.result import handle_result

router = APIRouter()


@router.post("/")
async def get_recommend(input: InferenceInput, request: Request):
    inference_server: InferenceService = request.app.inference_server
    response = inference_server.get_result(input)
    return handle_result(response)
