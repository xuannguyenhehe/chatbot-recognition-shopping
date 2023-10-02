from pydantic import BaseModel


class InferenceInput(BaseModel):
    path_image: str