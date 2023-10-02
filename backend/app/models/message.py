from pydantic import BaseModel
from typing import Optional
import datetime

class Message(BaseModel):
    message: str
    username: str
    chat_id: int
    path_image: Optional[str]
    is_from_self: bool
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "message": "hello",
                "username": "user01",
                "chat_id": 0,
                "path_image": "image01",
                "is_from_self": True,
                "is_active": True,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
            }
        }
