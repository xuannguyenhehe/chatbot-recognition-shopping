from typing import List, Optional

from pydantic import BaseModel


class InfoImage(BaseModel):
    label: str
    stocking: int = 0
    description: Optional[str] = ""


class InfoImages(BaseModel):
    infos: List[InfoImage]

class MetaClothes(InfoImage):
    username: str
