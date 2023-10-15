from app.schemas.inference import InferenceInput, IntentInput
from app.utils.repsonse.result import handle_result
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/")
async def answer(request: Request, input: InferenceInput):
    response = await request.app.rasa_service.get_answer(input)
    return handle_result(response)


@router.post("/intent")
async def answer(request: Request, message: IntentInput):
    response = await request.app.rasa_service.get_intent(message)
    return handle_result(response)