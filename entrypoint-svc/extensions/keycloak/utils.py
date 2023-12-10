from functools import wraps

import requests
from fastapi import HTTPException, Request

from app.utils.repsonse.result import ResultResponse, handle_result
from extensions.keycloak import verify_user


def require_token(request: Request):
    # Check to see if it's in their session
    access_token = \
        request.headers.get("Authorization", "").replace("Bearer ", "")
    user_auth = verify_user(request.app.kc_openid.keycloak_openid, access_token)

    if user_auth["status_code"] == requests.codes.unauthorized:
        res = HTTPException(requests.codes.unauthorized, user_auth["message"])
        raise res

    request.state.user_auth = user_auth
