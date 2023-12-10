import requests
from keycloak.exceptions import (KeycloakAuthenticationError,
                                 KeycloakConnectionError, KeycloakGetError)

from extensions.keycloak.authorization_service import Authorization
from extensions.keycloak.exceptions import KeyloakAttributeError


def verify_user(kc_openid, access_token):
    """ authenticate user with each request received by access token

    Args:
        str: access token

    Returns:
        dict: {
            "message": message,
            "auth": Authorization object,
            "status_code": (401 unauthorized | 200 ok)
        }
    """
    user_auth = {
        "access_token":"",
        "auth": {},
        "tenant": "",
        "status_code": requests.codes.ok,
        "message": "Ok",
        "is_realm_admin":False,
        "user_id": ""
    }
    try:
        user_authorization = Authorization(kc_openid, access_token)
        
        if "admin-realm" in user_authorization.realm_role:
            user_auth["is_realm_admin"] = True
        
        user_auth["user_id"] = user_authorization.user_id
        user_auth["access_token"] = access_token
    except KeycloakAuthenticationError:
        user_auth["message"] = "Token is invalid or expired"
        user_auth["status_code"] = requests.codes.unauthorized
    except (KeycloakGetError, KeycloakConnectionError):
        user_auth["message"] = "Token does not exist"
        user_auth["status_code"] = requests.codes.unauthorized
    except KeyloakAttributeError as e:
        user_auth["message"] = str(e)
        user_auth["status_code"] = requests.codes.unauthorized

    return user_auth
