from typing import List

import requests
from fastapi import APIRouter, Depends, Request

from app.schemas.qa import QAValid, QAValids
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


@router.post("/", response_model=QAValids, dependencies=[Depends(require_token)])
async def create(request: Request, qa_inputs: QAValids):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    if  'admin-realm' not in user_info['realm_role']:
        return handle_result(ResultResponse((
            f"Disallow to create a rasa model",
            requests.codes.unauthorized
        )))
    
    response = QAService(request.app.db).create(username=username, qa_inputs=qa_inputs)
    return handle_result(response)
