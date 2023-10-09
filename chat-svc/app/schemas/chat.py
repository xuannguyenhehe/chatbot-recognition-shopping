from pydantic import BaseModel


class Chat(BaseModel):
    name: str
    username: str
    current_entities: list