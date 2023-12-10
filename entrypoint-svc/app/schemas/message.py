import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.image import ImageInput


class MessageBase(BaseModel):
    chat_user: str
    is_backup: Optional[bool] = False
    offset_image: Optional[int] = 0

class MessageInput(BaseModel):
    content: str
    image: Optional[ImageInput]

class MessageOutput(BaseModel):
    message: str
    path_image: Optional[str]
    options: Optional[list] = None
    sender: str
    receiver: str

class CreatedMessages(MessageBase):
    message: MessageInput

class MessageResponse(MessageInput):
    created_date: datetime.datetime
    updated_date: datetime.datetime

class ChoseImageOfMessage(BaseModel):
    path_image: str
    chat_user: str

class SpecifiedMessage(BaseModel):
    message: str
    chat_user: str
