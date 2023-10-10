from pydantic import BaseModel
from typing import Optional
import datetime

class Message(BaseModel):
    message: str
    sender: str
    receiver: str
    chat_id: int
    is_chatbot: bool = False
    path_image: Optional[str]
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "message": "hello",
                "sender": "user01",
                "receiver": "user02",
                "chat_id": 0,
                "is_chatbot": False,
                "path_image": "image01",
                "is_active": True,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
            }
        }
