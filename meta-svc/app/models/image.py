import datetime
from typing import Any

from pydantic import BaseModel


class ImageVector(BaseModel):
    path: str
    name: str
    height: int
    width: int
    volume: int
    username: str
    label: str
    vector: Any
    pseudo_cate: dict
    pseudo_attr: dict
    pseudo_color: dict
    is_active: bool = True
    created_date: str = str(datetime.datetime.now())
    updated_date: str = str(datetime.datetime.now())
