from pydantic import BaseModel
from typing import Optional, List


class InferenceInput(BaseModel):
    path_image: Optional[str]
    colors: Optional[List[str]]
    category: Optional[str]
    attribute: Optional[str]


class InferenceColorInput(BaseModel):
    path_image: str