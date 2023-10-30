import datetime
import uuid

from pydantic import BaseModel


class Image(BaseModel):
    uuid: str = str(uuid.uuid4())
    path: str
    name: str
    height: int
    width: int
    volume: int
    username: str
    label: str
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "uuid": str(uuid.uuid4()),
                "path": "/",
                "name": "abc.jpg",
                "height": "100",
                "width": "100",
                "volume": "100",
                "username": "abc",
                "label": "shirt",
                "is_active": True,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
            }
        }
