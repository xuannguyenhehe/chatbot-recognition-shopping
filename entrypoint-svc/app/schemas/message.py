from pydantic import BaseModel
import datetime
from typing import Optional
from app.schemas.image import ImageInput

class MessageBase(BaseModel):
    chat_id: int

class MessageInput(BaseModel):
    message: str
    image: Optional[ImageInput]
    receiver: str

class MessageOutput(BaseModel):
    message: str
    path_image: Optional[str]
    receiver: str

class CreatedMessages(MessageBase):
    message: MessageInput

class MessageResponse(MessageInput):
    created_date: datetime.datetime
    updated_date: datetime.datetime