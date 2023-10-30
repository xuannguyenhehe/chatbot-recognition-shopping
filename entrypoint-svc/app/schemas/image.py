from pydantic import BaseModel


class ImageItem(BaseModel):
    path: str
    height: int
    width: int
    usage: str


class ImageInput(BaseModel):
    data: str
    filename: str
