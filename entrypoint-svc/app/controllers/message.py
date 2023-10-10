from fastapi import APIRouter, Request, Depends
from typing import List
from app.schemas.message import MessageResponse, CreatedMessages
from app.utils.repsonse.result import handle_result
from extensions.keycloak.utils import require_token
from app.services.message import MessageService
from app.utils.repsonse.result import ResultResponse
import requests

router = APIRouter(prefix="/message")


@router.get("/", response_model = List[MessageResponse], dependencies=[Depends(require_token)])
async def get(request: Request, chat_id: int):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    response = MessageService(request.app.db).get(chat_id, username)
    return handle_result(response)


@router.post("/", response_model = MessageResponse, dependencies=[Depends(require_token)])
async def create(request: Request, message: CreatedMessages):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    sender = user_info['preferred_username']

    if sender == message.message.receiver:
        return handle_result(ResultResponse((
            f"Can not create a message yourself",
            requests.codes.unauthorized
        )))
    
    response = MessageService(request.app.db).create(
        request.app.storage,
        message.chat_id, 
        message.message,
        sender,
    )
    return handle_result(response)
