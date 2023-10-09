from pydantic import BaseModel
import datetime
import uuid

class Image(BaseModel):
    uuid: str = str(uuid.uuid4())
    path: str
    height: int
    width: int
    volume: int
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "uuid": str(uuid.uuid4()),
                "path": "/",
                "height": "100",
                "width": "100",
                "volume": "100",
                "usage": "train",
                "is_active": True,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
            }
        }