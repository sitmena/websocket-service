from pydantic import BaseModel


class Message(BaseModel):
    token: str
    message: str
