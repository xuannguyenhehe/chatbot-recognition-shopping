from pydantic import BaseModel


class InferenceInput(BaseModel):
    sender: str
    message: str
