from app.schemas.inference import InferenceInput
from app.utils.repsonse.result import handle_result
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/")
async def answer(request: Request, input: InferenceInput):
    response = request.rasa_service.get_answer(input)
    return handle_result(response)


@router.post("/intent")
async def answer(request: Request, input: InferenceInput):
    response = request.rasa_service.get_intent(input)
    return handle_result(response)