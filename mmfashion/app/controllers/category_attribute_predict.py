from app.schemas.inference import InferenceInput
from app.utils.repsonse.result import handle_result
from fastapi import APIRouter, Request

router = APIRouter(prefix="/cap")


@router.post("/")
async def get_attribute(
    input: InferenceInput, 
    request: Request,
):
    response = request.app.state.cap_service.get_result(input.path_image)
    return handle_result(response)
