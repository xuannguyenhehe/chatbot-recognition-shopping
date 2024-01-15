import datetime
import uuid

from pydantic import BaseModel


class RasaCheckpoint(BaseModel):
    path: str
    username: str
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()
