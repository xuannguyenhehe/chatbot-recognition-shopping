from app.schemas.keycloak import AccessToken, UserRegister
from app.services.keycloak import KeycloakUserService
from app.utils.repsonse.result import handle_result
from extensions.keycloak.utils import require_token
from fastapi import APIRouter, Request, Depends
from typing import Annotated

router = APIRouter(prefix="/keycloak")

@router.post("/token")
def get_token(request: Request, access_token: AccessToken):
    """Get access token

    Args:
        user_auth (dict): dict of auth, message and status_code

    Returns:
        Response: Response
    """
    username = access_token.username
    password = access_token.password
    refresh_token = access_token.refresh_token
    if refresh_token:
        res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid).get_token_refresh(
            refresh_token=refresh_token
    )
    else:
        res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid).get_token_creds(
            username=username,
            password=password
        )
    return handle_result(res)


@router.post('/register')
def register_user(request: Request, user_register: UserRegister):
    """Register new user

    Returns:
        Response: Response
    """
    payload = {
        "username": user_register.username,
        "enabled": True,
        "credentials": [{
            "value": user_register.password, 
            "type": "password",
        }]
    }
    res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid)\
        .register_user(payload=payload)

    return handle_result(res)


@router.get('/user', dependencies=[Depends(require_token)])
def get_user_info(request: Request):
    """Get user info

    Args:
        user_auth (dict): dict of auth, message and status_code

    Returns:
        Response: Response
    """

    res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid)\
        .get_user_info(access_token=request.state.user_auth['access_token'])

    return handle_result(res)
