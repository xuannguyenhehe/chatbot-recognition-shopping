from pydantic import BaseModel
from typing import List


class ChatBotImage(BaseModel):
    name: str
    urls: List[str]


class ChatBotImages(BaseModel):
    images: List[ChatBotImage]