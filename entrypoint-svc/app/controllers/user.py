from fastapi import APIRouter, Depends, Request
from app.schemas.user import UserLogin, UserRegister
from app.services.user import UserService
from app.utils.repsonse.result import handle_result
from config import config


router = APIRouter(prefix="/user")


@router.post("/login")
async def login(request: Request, user: UserLogin):
    response = UserService(request.app.db).login(user)
    return handle_result(response)


@router.post("/register")
async def register(request: Request, user: UserRegister):
    response = UserService(request.app.db).register(user)
    return handle_result(response)