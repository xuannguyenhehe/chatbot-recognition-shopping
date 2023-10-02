from fastapi import APIRouter
from app.schemas.inference import InferenceInput
from app.services.inference import InferenceService
from app.utils.repsonse.result import handle_result


router = APIRouter(prefix="/answer")


@router.post("/")
async def answer(input: InferenceInput):
    response = InferenceService().get_answer(input)
    return handle_result(response)

@router.post("/intent")
async def answer(input: InferenceInput):
    response = InferenceService().get_intent(input)
    return handle_result(response)