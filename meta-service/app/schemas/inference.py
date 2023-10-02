from pydantic import BaseModel
from typing import Optional

class InferenceInput(BaseModel):
    entities: list
    path_image: Optional[str]
