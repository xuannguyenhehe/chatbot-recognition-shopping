from typing import List

import requests
from fastapi import APIRouter, Depends, Request

from app.schemas.rasa import RasaValid
from app.services.rasa import RasaModelService
from app.utils.repsonse.result import ResultResponse, handle_result
from extensions.keycloak.utils import require_token

router = APIRouter()


@router.get("/", response_model=RasaValid, dependencies=[Depends(require_token)])
async def get_by_user(request: Request):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    response = RasaModelService(request.app.db).get(username)
    return handle_result(response)


@router.post("/", response_model=RasaValid, dependencies=[Depends(require_token)])
async def create(request: Request):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    if  'admin-realm' not in user_info['realm_role']:
        return handle_result(ResultResponse((
            f"Disallow to create a rasa model",
            requests.codes.unauthorized
        )))
    
    response = RasaModelService(request.app.db).create(username=username)
    return handle_result(response)


@router.post("/approve", dependencies=[Depends(require_token)])
async def approve(request: Request):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    if  'admin-realm' not in user_info['realm_role']:
        return handle_result(ResultResponse((
            f"Disallow to create a rasa model",
            requests.codes.unauthorized
        )))
    
    response = RasaModelService(request.app.db).approve(username=username)
    return handle_result(response)

@router.get("/status-train", dependencies=[Depends(require_token)])
async def check_status_train(request: Request):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    if  'admin-realm' not in user_info['realm_role']:
        return handle_result(ResultResponse((
            f"Disallow to create a rasa model",
            requests.codes.unauthorized
        )))
    
    response = RasaModelService(request.app.db).check_status_train(username=username)
    return handle_result(response)
