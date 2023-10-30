from typing import List

import requests
from fastapi import APIRouter, Depends, Request

from app.schemas.message import CreatedMessages, MessageResponse
from app.services.message import MessageService
from app.utils.repsonse.result import ResultResponse, handle_result
from extensions.keycloak.utils import require_token

router = APIRouter()


@router.get("/", response_model = List[MessageResponse], dependencies=[Depends(require_token)])
async def get(request: Request, chat_user: str):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    response = MessageService(request.app.db).get(username, chat_user)
    return handle_result(response)


@router.post("/", response_model = MessageResponse, dependencies=[Depends(require_token)])
async def create(request: Request, message: CreatedMessages):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    sender = user_info['preferred_username']

    if sender == message.chat_user:
        return handle_result(ResultResponse((
            f"Can not create a message yourself",
            requests.codes.unauthorized
        )))
    
    response = MessageService(request.app.db).create(
        request.app.storage,
        message.chat_user, 
        message.message,
        sender,
    )
    return handle_result(response)
