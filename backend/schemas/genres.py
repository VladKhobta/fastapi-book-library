from typing import Optional, List

from pydantic import BaseModel


class TunedModel(BaseModel):

    class Config:
        from_attributes = True


class GenreCreation(BaseModel):
    name: str


class GenreShowing(TunedModel):
    name: str
