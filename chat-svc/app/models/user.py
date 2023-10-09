import datetime
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    hash_password: str
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "username": "abc",
                "hash_password": "abc",
                "is_active": True,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
            }
        }

