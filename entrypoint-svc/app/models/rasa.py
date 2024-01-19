import datetime
from typing import Optional

from pydantic import BaseModel


class RasaCheckpoint(BaseModel):
    path: Optional[str] = None
    username: str
    status: str
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()
