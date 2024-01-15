import datetime
import uuid

from pydantic import BaseModel


class QA(BaseModel):
    username: str
    answer: str
    question: list
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()
