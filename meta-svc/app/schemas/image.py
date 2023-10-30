from typing import List

from pydantic import BaseModel


class ChatBotImage(BaseModel):
    name: str
    urls: List[str]


class ChatBotImages(BaseModel):
    images: List[ChatBotImage]
