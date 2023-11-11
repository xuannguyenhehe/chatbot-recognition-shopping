import datetime
from typing import List

from pydantic import BaseModel


class MetaClothes(BaseModel):
    id: int
    label: str
    description: str
    list_image_ids: List[int]
    stocking: int
    is_active: bool = True
    created_date: str = str(datetime.datetime.now())
    updated_date: str = str(datetime.datetime.now())
