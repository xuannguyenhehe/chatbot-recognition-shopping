import ast

import requests
from app.utils.repsonse.result import ResultResponse
from config import config
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakError
from loguru import logger


class KeycloakUserService:
    def __init__(self, kc_admin, kc_openid):
        self.kc_admin = kc_admin.admin
        self.kc_openid = kc_openid.keycloak_openid

    def get_token_creds(self, username, password):
        try:
            data = self.kc_openid.token(
                username=username,
                password=password,
                grant_type='password'
            )
            value = {
                'access_token':data['access_token'],
                'refresh_token':data['refresh_token'] 
            }
            return ResultResponse((
                'Successfully get user token', 
                requests.codes.ok, 
                value,
            ))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))
 
    def get_token_refresh(self, refresh_token):
        try:
            data = self.kc_openid.refresh_token(refresh_token)
            value = {
                'access_token':data['access_token'],
                'refresh_token':data['refresh_token'] 
            }
            return ResultResponse(('Successfully get user token', requests.codes.ok, value))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def register_user(self, payload):
        try:
            data = self.kc_admin.create_user(payload)
            return ResultResponse(('Successfully create new user', requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def get_user_info(self, access_token):
        try:
            data = self.kc_openid.userinfo(access_token)
            return ResultResponse(('Successfully get new user info', requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def get_groups(self):
        try:
            data = self.kc_admin.get_groups()
            return ResultResponse(('Successfully getgroup info', requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def get_group_members(self, group_id):
        try:
            data = self.kc_admin.get_group_members(group_id)
            msg = 'Successfully get group member info'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def get_realm_roles(self):
        try:
            data = self.kc_admin.get_realm_roles()
            msg = 'Successfully get group member info'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))
        
    def get_group_roles(self, group_id):
        try:
            data = self.kc_admin.get_group_realm_roles(group_id)
            msg = 'Successfully get group role info'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def get_realm_roles_of_user(self, user_id):
        try:
            data = self.kc_admin.get_realm_roles_of_user(
                user_id=user_id
                )
            msg = 'Successfully get user role info'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def add_user_role(self, user_id, roles):
        if not isinstance(roles, list):
            roles = [roles]
        try:
            data = self.kc_admin.assign_realm_roles(
                user_id=user_id,
                roles=roles
                )
            msg = 'Successfully add user role'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def delete_user_role(self, user_id, roles):
        if not isinstance(roles, list):
            roles = [roles]
        try:
            data = self.kc_admin.delete_realm_roles_of_user(
                user_id=user_id,
                roles=roles
                )
            msg = 'Successfully delete user role'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def update_user(self, user_id, payload):
        try:
            data = self.kc_admin.update_user(
                user_id=user_id,
                payload=payload
                )
            msg = 'Successfully update user info'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def logout(self, user_id):
        try:
            data = self.kc_admin.user_logout(
                user_id=user_id
                )
            msg = 'Successfully logout'
            return ResultResponse((msg, requests.codes.ok, data))

        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def reset_user_password(self,
                            username,
                            user_id,
                            password,
                            new_password,
                            temporary=True):

        try:
            # valid user credentials
            KeycloakAdmin(
                server_url=config['KEYCLOAK_URL'],
                username=username,
                password=password,
                realm_name=config["REALMS"],
                verify=True
            )
            # update to new password
            data = self.kc_admin.set_user_password(
                user_id=user_id,
                password=new_password,
                temporary=temporary
            )
            msg = 'Successfully update user passwordt'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    def reset_user_password_by_admin(
        self,
        user_reset_id,
        user_id,
        new_password,
        temporary=True,
    ):
        try:
            # update to new password
            data = self.kc_admin.set_user_password(
                user_id=user_reset_id,
                password=new_password,
                temporary=temporary
            )
            msg = 'Successfully update password'
            return ResultResponse((msg, requests.codes.ok, data))
        except KeycloakError as e:
            res = self.return_keycloak_error(e)
            logger.error(f"[Keycloak Error] {res}")
            return ResultResponse((res, requests.codes.bad_request))

    @staticmethod
    def return_keycloak_error(e):
        e = ast.literal_eval(e.error_message\
                .decode('utf-8'))
        res = e.get('error_description','')
        if not res:
            res = e.get('error','')
        return res