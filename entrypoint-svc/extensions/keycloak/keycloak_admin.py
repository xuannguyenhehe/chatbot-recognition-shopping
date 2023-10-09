from keycloak import KeycloakAdmin
 
class KeycloakAdminConnector:
    def __init__(self):
        self.admin = None

    def init_app(self, config):
        config["KEYCLOAK_SECURE"] = True
        self.admin = self.connect(config)

    def connect(self, config):
        return KeycloakAdmin(
            server_url=config["KEYCLOAK_URL"],
            username=config['KEYCLOAK_ADMIN_USERNAME'],
            password=config['KEYCLOAK_ADMIN_PASSWORD'],
            realm_name=config["REALMS"],
            verify=config["KEYCLOAK_SECURE"],
        )
    

    def refresh_credentials(self):
        self.admin.refresh_token()
