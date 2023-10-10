from app.schemas.keycloak import AccessToken, UserRegister, RoleByUser
from app.services.keycloak import KeycloakUserService
from app.utils.repsonse.result import handle_result
from extensions.keycloak.utils import require_token
from fastapi import APIRouter, Request, Depends
from app.utils.repsonse.result import ResultResponse
import requests


router = APIRouter(prefix="/keycloak")

@router.post("/token")
def get_token(request: Request, access_token: AccessToken):
    """Get access token"""
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
    """Register new user"""

    payload = {
        "username": user_register.username,
        "enabled": True,
        "credentials": [{
            "value": user_register.password, 
            "type": "password",
        }]
    }
    res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid).register_user(payload=payload)

    return handle_result(res)


@router.post('/user/role', dependencies=[Depends(require_token)])
def add_user_role(request: Request, role: RoleByUser):
    """add role for user"""

    is_exist_role = False
    role_config = None
    for element_role in request.app.kc_admin.admin.get_realm_roles():
        if role.role == element_role['name']:
            is_exist_role = True
            role_config = element_role
    
    if not is_exist_role:
        return handle_result(ResultResponse((
            f"No exist {role.role}",
            requests.codes.unauthorized
        )))
    
    user_auth = request.state.user_auth
    user_id = user_auth["user_id"]

    user_roles = request.app.kc_admin.admin.get_realm_roles_of_user(user_id=user_id)
    is_available_role = [element_role for element_role in user_roles if element_role['name'] == role.role]
    if len(is_available_role):
        return handle_result(ResultResponse((
            f"This user exist any role",
            requests.codes.unauthorized,
        )))
    
    res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid).add_user_role(
        user_id=user_id,
        roles=role_config,
    )

    return handle_result(res)


@router.get('/user', dependencies=[Depends(require_token)])
def get_user_info(request: Request):
    """Get user info"""

    res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid)\
        .get_user_info(access_token=request.state.user_auth['access_token'])

    return handle_result(res)


@router.get('/roles')
def get_all_realm_roles(request: Request):
    """Get all realm roles"""

    res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid).get_realm_roles()

    return handle_result(res)


@router.get('/user/roles', dependencies=[Depends(require_token)])
def get_roles_of_user(request: Request):
    """Get all user roles"""
    # check if is realm admin
    user_auth = request.state.user_auth
    if not user_auth["is_realm_admin"]:
        return handle_result(ResultResponse((
            "Provided access token does not have administrative privileges to request this api",
            requests.codes.unauthorized
        )))
    
    user_id = user_auth["user_id"]
    res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid).get_realm_roles_of_user(user_id=user_id)

    return handle_result(res)


@router.get('/users', dependencies=[Depends(require_token)])
def get_all_user(request: Request):
    """Get user info

    Args:
        user_auth (dict): dict of auth, message and status_code

    Returns:
        Response: Response
    """

    res = KeycloakUserService(request.app.kc_admin, request.app.kc_openid)\
        .get_all_name_users()

    return handle_result(res)