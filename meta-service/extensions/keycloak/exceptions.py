from keycloak.exceptions import KeycloakError


class KeyloakAttributeError(KeycloakError):
    """Exception for invalid attribute in auth"""
    pass