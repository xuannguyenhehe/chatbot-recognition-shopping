from fastapi import APIRouter, Depends
from app.models import get_database
from app.schemas.user import UserLogin, UserRegister
from app.services.user import UserService
from app.utils.repsonse.result import handle_result


router = APIRouter(prefix="/user")


@router.post("/login")
async def login(user: UserLogin, db: get_database = Depends()):
    response = UserService(db).login(user)
    return handle_result(response)


@router.post("/register")
async def register(user: UserRegister, db: get_database = Depends()):
    response = UserService(db).register(user)
    return handle_result(response)