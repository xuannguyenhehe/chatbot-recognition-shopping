from fastapi import APIRouter, Request

from app.schemas.train import TrainInput
from app.utils.repsonse.result import handle_result
from app.services.train import TrainService
from extensions.minio.connector import MinioConnector

router = APIRouter()


@router.post("/")
async def answer(request: Request, input: TrainInput):
    train_service : TrainService = request.app.train_service
    response = await train_service.train(input.username, input.data)
    return handle_result(response)

