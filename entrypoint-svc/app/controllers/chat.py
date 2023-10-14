from fastapi import APIRouter, Request, Depends
from app.schemas.chat import Chat
from app.services.chat import ChatService
from app.utils.repsonse.result import handle_result
from extensions.keycloak.utils import require_token
from typing import List
from app.utils.repsonse.result import ResultResponse
import requests


router = APIRouter()


@router.get("/", response_model=List[Chat], dependencies=[Depends(require_token)])
async def get_by_user(request: Request, is_get_last_message: bool = True):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    response = ChatService(request.app.db).get(username, is_get_last_message)
    return handle_result(response)


@router.post("/", response_model=Chat, dependencies=[Depends(require_token)])
async def create(request: Request, chat: Chat):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    usernames = list(set([data['username'] for data in request.app.kc_admin.admin.get_users({})]) - {'chatbot'})
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    sender = user_info['preferred_username']

    if chat.receiver not in usernames or chat.receiver == user_info['preferred_username']:
        return handle_result(ResultResponse((
            f"Can not create a chat with {chat.receiver}",
            requests.codes.unauthorized
        )))
    
    response = ChatService(request.app.db).create(chat, sender)
    return handle_result(response)