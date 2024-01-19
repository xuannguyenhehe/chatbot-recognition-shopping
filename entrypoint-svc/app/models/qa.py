import datetime
from typing import List

from pydantic import BaseModel


class QA(BaseModel):
    keyword: str
    username: str
    answer: str
    questions: List[str]
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()
