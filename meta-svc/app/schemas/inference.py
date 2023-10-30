from typing import List, Optional

from pydantic import BaseModel


class InferenceInput(BaseModel):
    path_image: Optional[str]
    colors: Optional[List[str]]
    category: Optional[str]
    attribute: Optional[dict]


class InferenceColorInput(BaseModel):
    path_image: str
