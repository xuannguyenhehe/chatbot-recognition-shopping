import datetime
import uuid

from pydantic import BaseModel


class Image(BaseModel):
    path: str
    username: str
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "path": "/",
                "username": "abc",
                "is_active": True,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
            }
        }
