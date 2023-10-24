from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update
from sqlalchemy import select, func

from uuid import UUID
from typing import List, Union

from db.models import Book, Author


class AuthorDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            name: str
    ) -> Author:
        new_author = Author(
            name=name
        )

        self.session.add(new_author)
        await self.session.commit()
        return new_author

    async def get_by_id(
            self,
            author_id: UUID
    ) -> Union[Author, None]:
        query = select(Author).where(Author.id == author_id)
        res = await self.session.execute(query)
        author_row = res.fetchone()
        if author_row:
            return author_row[0]

    async def get_by_name(
            self,
            name: str
    ) -> Union[Author, None]:
        query = select(Author).where(Author.name == name)
        res = await self.session.execute(query)
        author_row = res.fetchone()
        if author_row:
            return author_row[0]

    async def get_all(self) -> List[Author]:
        res = await self.session.execute(select(Author))
        return res.scalars().all()

    async def update(
            self,
            author_id: UUID,
            **kwargs
    ) -> Union[Author, None]:
        query = (
            update(Author)
            .where(Author.id == author_id)
            .values(kwargs)
            .returning(Author)
        )
        res = await self.session.execute(query)
        updated_row = res.fetchone()
        if updated_row:
            return updated_row[0]
