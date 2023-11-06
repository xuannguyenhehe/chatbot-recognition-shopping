from typing import List, Optional

from pydantic import BaseModel


class InferenceInput(BaseModel):
    username: str
    path_image: Optional[str]
    colors: Optional[List[str]]
    category: Optional[List[str]]
    attribute: Optional[List[str]]
