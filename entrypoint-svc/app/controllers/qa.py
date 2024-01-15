from typing import List

import requests
from fastapi import APIRouter, Depends, Request

from app.schemas.qa import QAValid
from app.services.qa import QAService
from app.utils.repsonse.result import ResultResponse, handle_result
from extensions.keycloak.utils import require_token

router = APIRouter()


@router.get("/", response_model=QAValid, dependencies=[Depends(require_token)])
async def get_by_user(request: Request):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    response = QAService(request.app.db).get(username)
    return handle_result(response)


@router.post("/", response_model=QAValid, dependencies=[Depends(require_token)])
async def create(request: Request, qa_input: QAValid):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)

    if  user_info['role'] != 'realm-admin':
        return handle_result(ResultResponse((
            f"Disallow to create a rasa model",
            requests.codes.unauthorized
        )))
    
    response = QAService(request.app.db).create(qa_input)
    return handle_result(response)
