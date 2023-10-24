from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class TunedModel(BaseModel):

    class Config:
        from_attributes = True


class BookCreation(BaseModel):
    title: str
    authors: List[str]
    genre: Optional[str] = None


class BookShowing(TunedModel):
    title: str
    authors: List[str]
    genre_id: Optional[UUID] = None
