from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput
from app.utils.repsonse.result import handle_result

router = APIRouter(prefix="/apc")


@router.post("/")
async def get_attribute(
    input: InferenceInput, 
    request: Request,
):
    response = request.app.state.apc_service.get_result(input.path_image)
    return handle_result(response)
