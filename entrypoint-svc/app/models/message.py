import datetime
from typing import Optional, Any

from pydantic import BaseModel


class Message(BaseModel):
    message: str
    sender: str
    receiver: str
    chat_id: int
    is_chatbot: bool = False
    path_image: Optional[str]
    options: Optional[Any]
    is_option_action: Optional[bool]
    is_active: bool = True
    created_date: datetime.datetime = datetime.datetime.now()
    updated_date: datetime.datetime = datetime.datetime.now()
