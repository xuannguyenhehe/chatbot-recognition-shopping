from pydantic import BaseModel
import datetime

class Chat(BaseModel):
    id: int
    sender: str
    receiver: str
    is_active: bool = True
    current_entities: list = []
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "sender": "abc",
                "receiver": "abc",
                "is_active": True,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
            }
        }