from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update
from sqlalchemy import select, func

from uuid import UUID
from typing import List, Union

from db.models import Genre


class GenreDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            name: str
    ) -> Genre:
        new_genre = Genre(
            name=name
        )

        self.session.add(new_genre)
        await self.session.commit()
        return new_genre

    async def get_by_name(
            self,
            name: str
    ) -> Union[Genre, None]:
        query = select(Genre).where(Genre.name == name)
        res = await self.session.execute(query)
        genre_row = res.fetchone()
        if genre_row:
            return genre_row[0]

    async def get_all(self) -> List[Genre]:
        res = await self.session.execute(select(Genre))
        return res.scalars().all()
