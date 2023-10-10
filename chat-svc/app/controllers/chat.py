from fastapi import APIRouter, Depends
from app.models import get_database
from app.schemas.chat import Chat
from app.services.chat import ChatService
from app.utils.repsonse.result import handle_result
from typing import List


router = APIRouter(prefix="/chat")


@router.get("/", response_model=List[Chat])
async def get_by_user(username: str, db: get_database = Depends()):
    response = ChatService(db).get(username)
    return handle_result(response)


@router.post("/", response_model=Chat)
async def create(chat: Chat, db: get_database = Depends()):
    response = ChatService(db).create(chat)
    return handle_result(response)