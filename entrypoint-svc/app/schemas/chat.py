from typing import Optional

from pydantic import BaseModel


class Chat(BaseModel):
    receiver: str
    current_entities: Optional[list]

class NewChat(BaseModel):
    username: str
    current_entities: Optional[list]
