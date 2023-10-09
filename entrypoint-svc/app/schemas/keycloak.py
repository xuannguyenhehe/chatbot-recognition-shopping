from pydantic import BaseModel, validator
from typing import Optional


class AccessToken(BaseModel):
    username: str = None
    password: str = None
    refresh_token: str = None

    @validator('refresh_token')
    def check_password_or_refresh_token(cls, field_value, values):
        if 'username' not in values and 'password' not in values and not field_value:
            raise ValueError('Either password or refresh token is required.')
        return field_value


class UserRegister(BaseModel):
    username: str
    password: str
    repassword: str

    @validator('repassword')
    def check_repassword(cls, field_value, values):
        if values['password'] != field_value:
            raise ValueError('Repassword and password need to be same.')
        return field_value