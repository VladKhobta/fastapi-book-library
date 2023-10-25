from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from uuid import UUID
from typing import List, Union

from db.models import Book, Author, BookAuthor, Genre


class BookDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            title: str,
            genre: Genre,
            authors: List[Author],
    ):
        new_book = Book(
            title=title,
            genre_id=genre.id if genre else None,
        )

        self.session.add(new_book)
        await self.session.commit()

        book_authors = []
        for author in authors:
            book_authors.append(BookAuthor(
                book_id=new_book.id,
                author_id=author.id
            ))

        self.session.add_all(book_authors)
        await self.session.commit()
        return new_book

    async def get_by_id(
            self,
            book_id: UUID
    ) -> Union[Book, None]:
        query = (
            select(Book)
            .where(Book.id == book_id)
            .options(
                selectinload(Book.authors)
            )
        )
        res = await self.session.execute(query)
        book_row = res.fetchone()
        if book_row:
            return book_row[0]

    async def get_by_title(
            self,
            book_title: str
    ) -> Union[Book, None]:
        query = (
            select(Book)
            .where(Book.title == book_title)
            .options(
                selectinload(Book.authors)
            )
        )
        res = await self.session.execute(query)
        book_row = res.fetchone()
        if book_row:
            return book_row[0]

    async def get_all(
            self,
            skip: int,
            limit: int
    ) -> List[Book]:
        res = await self.session.execute(
            select(Book)
            .offset(skip)
            .limit(limit)
        )
        return res.scalars().all()

    async def delete(
            self,
            book_id: UUID
    ) -> UUID:
        res = await self.session.execute(
            select(Book)
            .where(Book.id == book_id)
            .options(
                selectinload(Book.authors)
            )
        )
        book = res.scalar_one()
        for author in book.authors:
            await self.session.delete(author)
        await self.session.delete(book)
        await self.session.commit()
        return book_id
