from pydantic import BaseModel
from typing import Optional


class Chat(BaseModel):
    name: str
    receiver: str
    current_entities: Optional[list]