from typing import Optional, List

from pydantic import BaseModel


class TunedModel(BaseModel):

    class Config:
        from_attributes = True


class AuthorCreation(BaseModel):
    name: str


class AuthorShowing(TunedModel):
    name: str


class AuthorUpdate(BaseModel):
    name: Optional[str]
