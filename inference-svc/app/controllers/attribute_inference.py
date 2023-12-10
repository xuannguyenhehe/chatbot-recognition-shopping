from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput
from app.services.attribute_inference import AttributePredictCoarseService
from app.utils.repsonse.result import handle_result

router = APIRouter()


@router.post("/")
async def get_attribute(input: InferenceInput, request: Request):
    inference_service: AttributePredictCoarseService = request.app.attribute_inference_server
    response = inference_service.get_result(input.path_image)
    return handle_result(response)
