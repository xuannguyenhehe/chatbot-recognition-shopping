from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput
from app.services.color_inference import ColorInferenceService
from app.utils.repsonse.result import handle_result

router = APIRouter()


@router.post("/")
async def get_color(input: InferenceInput, request: Request):
    inference_server: ColorInferenceService = request.app.color_inference_server
    response = inference_server.get_colors(input.path_image)
    return handle_result(response)


