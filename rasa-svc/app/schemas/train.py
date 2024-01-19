from pydantic import BaseModel
from typing import List

class TrainIntent(BaseModel):
    questions: List[str]
    answer: str
    keyword: str

class TrainIntents(BaseModel):
    intents: List[TrainIntent]

class TrainInput(BaseModel):
    username: str
    data: TrainIntents

