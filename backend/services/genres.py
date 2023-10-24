from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union, List

from schemas.genres import GenreShowing, GenreCreation
from db.session import get_session
from db.dals import GenreDAL

from uuid import UUID


class GenreService:

    def __init__(
            self,
            session: AsyncSession = Depends(get_session)
    ):
        self.session = session

    async def create(
            self,
            body: GenreCreation
    ) -> UUID:
        genre_dal = GenreDAL(self.session)
        new_genre = await genre_dal.create(name=body.name)
        return new_genre.id

    async def get_by_name(
            self,
            name: str
    ) -> Union[GenreShowing, None]:
        genre_dal = GenreDAL(self.session)
        genre = await genre_dal.get_by_name(name=name)
        if genre:
            return GenreShowing(name=genre.name)

    async def get_all(self) -> List[GenreShowing]:
        genre_dal = GenreDAL(self.session)
        genres = await genre_dal.get_all()
        return [GenreShowing(name=genre.name) for genre in genres]
