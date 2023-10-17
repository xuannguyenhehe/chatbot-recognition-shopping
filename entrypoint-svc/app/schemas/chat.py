from pydantic import BaseModel
from typing import Optional


class Chat(BaseModel):
    receiver: str
    current_entities: Optional[list]

class NewChat(BaseModel):
    username: str
    current_entities: Optional[list]