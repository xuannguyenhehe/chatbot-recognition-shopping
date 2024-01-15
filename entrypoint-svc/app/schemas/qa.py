from pydantic import BaseModel
from typing import List


class QAValid(BaseModel):
    question: List[str]
    answer: str
