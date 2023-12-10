from keycloak import KeycloakOpenID


class KeycloakOpenIDConnector:
    def __init__(self):
        self.keycloak_openid = None

    def init_app(self, config):
        config["KEYCLOAK_SECURE"] = True
        self.keycloak_openid = self.connect(config)

    def connect(self, config):
        return KeycloakOpenID(
            server_url=config["KEYCLOAK_URL"],
            client_id=config["KEYCLOAK_CLIENT_ID"],
            client_secret_key=config["KEYCLOAK_SECRET_KEY"],
            realm_name=config["REALMS"],
            verify=config["KEYCLOAK_SECURE"],
        )
