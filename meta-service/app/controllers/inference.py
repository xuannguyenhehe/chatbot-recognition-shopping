from fastapi import APIRouter, Request
from app.schemas.inference import InferenceInput
from app.services.inference import InferenceService
from app.utils.repsonse.result import handle_result


router = APIRouter()


@router.post("/")
async def get_recommend(
    input: InferenceInput, 
    request: Request,
):
    response = InferenceService(
        storage=request.app.state.storage,
        vector_search=request.app.state.vector_search,
        db=request.app.state.db,
    ).get_result(input)
    return handle_result(response)


@router.post("/update_pseudo")
async def update_pseudo(
    request: Request,
):
    response = InferenceService(
        storage=request.app.state.storage,
        vector_search=request.app.state.vector_search,
        db=request.app.state.db,
    ).update_pseudo_color()
    return handle_result(response)
