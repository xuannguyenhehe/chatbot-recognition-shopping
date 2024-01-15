from pydantic import BaseModel


class RasaValid(BaseModel):
    path: str
