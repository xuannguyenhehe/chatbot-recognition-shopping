from app.schemas.inference import InferenceInput
from app.utils.repsonse.result import handle_result
from fastapi import APIRouter, Request
from app.services.attribute_predict_coarse import AttributePredictCoarseService

router = APIRouter()


@router.post("/")
async def get_attribute(
    input: InferenceInput, 
    request: Request,
):
    # response = AttributePredictCoarseService(request.app.storage, request.app.config).get_result(input.path_image)
    response = request.app.apc_service.get_result(input.path_image)
    return handle_result(response)
