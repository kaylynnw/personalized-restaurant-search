from pydantic import BaseModel


class Question(BaseModel):
    address: str
    dietaryRestrictions: str
