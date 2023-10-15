from pydantic import BaseModel


class InferenceInput(BaseModel):
    sender: str
    message: str

class IntentInput(BaseModel):
    message: str
