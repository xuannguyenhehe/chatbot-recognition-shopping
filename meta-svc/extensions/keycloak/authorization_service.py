from config import config
from extensions.keycloak.exceptions import KeyloakAttributeError


class Authorization:    
    def __init__(self, kc_openid, access_token: str):
        self.user_info = kc_openid.userinfo(access_token)
        if "realm_role" not in self.user_info:
            raise KeyloakAttributeError(
                "missing realm_role in access token"
            )

        self.realm_role = self.user_info["realm_role"]
        self.user_id = self.user_info["sub"]

    def verify_realm_role(self):
        return config["ADMIN_REALM_ROLE"] in self.realm_role

    def verify_services(self):
        return (
            self.user_client_role and
            set(config["CLIENT_ROLES_DEFAULT"]) & set(self.user_client_role)
        )
