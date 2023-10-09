from pydantic import BaseModel
from passlib.context import CryptContext


class UserLogin(BaseModel):
    username: str
    password: str


class HashUserLogin(BaseModel):
    username: str
    hash_password: str

    @staticmethod
    def verify_password(
        plain_password, 
        hashed_password, 
    ):
        pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd.verify(plain_password, hashed_password)


class UserRegister(BaseModel):
    username: str
    password: str
    repassword: str

    @staticmethod
    def get_password_hash(
        password: str, 
    ):
        pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        return pwd.hash(password)