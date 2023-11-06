import datetime
import uuid

from pydantic import BaseModel
from typing import Any


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
