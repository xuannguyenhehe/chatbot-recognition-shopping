from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput
from app.services.meta_inference import MetaInferenceService
from app.utils.repsonse.result import handle_result

router = APIRouter()


@router.post("/")
async def get_recommend(input: InferenceInput, request: Request):
    inference_server: MetaInferenceService = request.app.meta_inference_server
    response = inference_server.get_result(input.path_image)
    return handle_result(response)



