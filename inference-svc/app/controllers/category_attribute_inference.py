from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput
from app.utils.repsonse.result import handle_result
from app.services.category_attribute_inference import CategoryAttributePredictService

router = APIRouter()


@router.post("/")
async def get_attribute(input: InferenceInput, request: Request):
    inference_server: CategoryAttributePredictService = request.app.category_attribute_inference_server
    response = inference_server.get_result(input.path_image)
    return handle_result(response)
