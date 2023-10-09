from app.schemas.user import UserLogin, HashUserLogin, UserRegister
from app.utils.repsonse.exceptions import ExceptionResponse
from app.services import AppService, AppCRUD
from app.models.user import User
from app.utils.repsonse.result import ResultResponse
from fastapi import status

class UserService(AppService):
    def login(self, user: UserLogin) -> ResultResponse:
        exist_user = UserCRUD(self.db).get(user.username)
        if not exist_user:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "username": user.username,
            }))
        is_same = exist_user.verify_password(user.password, exist_user.hash_password)
        if not is_same:
            return ResultResponse(ExceptionResponse.WrongPassword())
        message = "Login successful"
        return ResultResponse((message, status.HTTP_200_OK))

    def register(self, user: UserRegister) -> ResultResponse:
        exist_user = UserCRUD(self.db).get(user.username)
        if exist_user:
            return ResultResponse(ExceptionResponse.ExistedError({
                "username": user.username,
            }))
        if not user.password == user.repassword:
            return ResultResponse(ExceptionResponse.RePassword())
        message, status_code = UserCRUD(self.db).create(user)
        return ResultResponse((message, status_code))


class UserCRUD(AppCRUD):
    def create(self, user: UserRegister) -> User:
        hash_password = user.get_password_hash(user.password)
        user = User(username=user.username, hash_password=hash_password)
        message, status_code = self.insert("User", self.serialize(user))
        return message, status_code

    def get(self, username: str) -> HashUserLogin:
        user = self.db.User.find_one({
            "username": username,
        })
        if user:
            return HashUserLogin(**user)
        return None
