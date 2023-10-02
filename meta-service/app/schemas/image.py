from pydantic import BaseModel


class ImageItem(BaseModel):
    path: str