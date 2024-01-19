from fastapi import APIRouter, Request

from app.schemas.inference import InferenceInput, IntentInput, CheckpointInput
from app.utils.repsonse.result import handle_result
from app.services.inference import InferenceService
from extensions.minio.connector import MinioConnector

router = APIRouter()


@router.post("/")
async def answer(request: Request, input: InferenceInput):
    inference_service : InferenceService = request.app.inference_service
    response = await inference_service.get_answer(input)
    return handle_result(response)


@router.post("/intent")
async def answer(request: Request, message: IntentInput):
    inference_service : InferenceService = request.app.inference_service
    response = await inference_service.get_intent(message)
    return handle_result(response)

@router.post("/approve")
async def approve(request: Request, checkpoint: CheckpointInput):
    inference_service : InferenceService = request.app.inference_service
    minio_client: MinioConnector = request.app.storage
    
    response = await inference_service.approve(minio_client, checkpoint.username)
    return handle_result(response)

@router.get("/status-train")
async def get_status_train(request: Request, username: str):
    inference_service : InferenceService = request.app.inference_service
    response = await inference_service.get_status_train(username)
    return handle_result(response)