from pydantic import BaseModel
from typing import List


class QAValid(BaseModel):
    keyword: str
    questions: List[str]
    answer: str

class QAValids(BaseModel):
    intents: List[QAValid]
